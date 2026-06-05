from django.db.models.manager import BaseManager
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Any, TypedDict
from datetime import datetime

from django.utils import timezone
from clinician_overview.models import AccessGrant, Client
from clinician_overview.scoring.dass21 import Dass21Score
from clinician_overview.scoring.dest import DesTScore
from clinician_overview.scoring.gse import GSEScore
from clinician_overview.scoring.itq_dichotomous import ItqDichotomousScore
from clinician_overview.scoring.pcl5_diagnostic import Pcl5Score
import clinician_overview.util.access as access
from clinician_overview.util.score_questionnaire_response import score_questionnaire_response
from initial_screening.decorators.clinician_decorator import clinician_required
from initial_screening.models import QuestionnaireResponse, FormMembership, ResponseItem
import calendar
from django.contrib.auth.decorators import login_required

import clinician_overview.util.get_client_information as get_client_information
from clinician_overview.util.get_client_information import ViewClientInfo

class SubmissionSummary(TypedDict):
    id: int
    form: str
    submission_date: datetime 
    results: str
    scheduled_deletion: datetime

@clinician_required
@login_required
def client_summary_page(request: HttpRequest, client_id: str) -> HttpResponse:
  clinician: User = cast(User, request.user)
  client: Client | None = clientm.find(client_id, clinician)
  if not client:
    return render(request, 'clinician_overview/client_not_found.html', { "client_id": client_id })

  access_grant = access.has_access(clinician, client)
  
  ctx = make_context(client, access_grant)
  return render(request, 'clinician_overview/client_summary_page.html', context=ctx)

def get_form_completion_date_for_client(client_id: Client, form_id: int)  -> datetime | None:
  last_questionnaire = FormMembership.objects.filter(form_id=form_id).order_by("order").last()
  if last_questionnaire:
    last_response = QuestionnaireResponse.objects.filter(user_identifier=client_id, form_id=form_id, questionnaire_id=last_questionnaire.questionnaire.id).order_by("submitted_at").last()

    if last_response:
      return last_response.submitted_at
    
def create_questionnaire_result_string(result: DesTScore | ItqDichotomousScore | Pcl5Score | Dass21Score | GSEScore) -> str:
  elevated_string = "Elevated - Priority Review"
  routine_string = "Within Range - Routine Review"
  if isinstance(result, DesTScore):
    return elevated_string if result.significant else routine_string
  elif isinstance(result, ItqDichotomousScore):
    return routine_string if result.diagnosis == "none" else elevated_string
  elif isinstance(result, Pcl5Score):
    return elevated_string if result.ptsd_indicated else routine_string
  elif isinstance(result, Dass21Score):
    return elevated_string if result.total >= 60 or result.depression >= 21 else routine_string
  else:
    # GSE
    return routine_string
  
  
def make_context(client_id: str) -> dict[str, Any]:
  try:
    client: Client = Client.objects.get(client_id=client_id)
    client_basic_information: ViewClientInfo = get_client_information.get_client_information(client_id)

    unique_form_names: list[str] = []
    access_grant = AccessGrant.objects.filter(client=client).first()
    if access_grant:
      access_renewed_date = access_grant.created_at
      access_expiry_date = access.has_access_until(client)
      access_status = "Expiring Soon" if access_expiry_date and access_expiry_date > timezone.now() else "Expired"
    else:
      access_renewed_date = None
      access_expiry_date = None
      access_status = "No Access"

    initial_screening_questionnaire_id = 3

    submissions: BaseManager[QuestionnaireResponse] = QuestionnaireResponse.objects.filter(user_identifier = client).exclude( questionnaire_id=initial_screening_questionnaire_id)

    formatted_submissions: list[SubmissionSummary] = []
    for sub in submissions:
      form_name = f"{sub.form.name}: {sub.questionnaire.name}"

      # calculate deletion date -- 6 months after the submitted date
      deletion_month = sub.submitted_at.month - 1 + 6 
      deletion_year = sub.submitted_at.year + deletion_month // 12 
      deletion_month = deletion_month % 12 + 1
      deletion_day = min(sub.submitted_at.day, calendar.monthrange(deletion_year, deletion_month)[1])

      responses = ResponseItem.objects.filter(response=sub)
      score: DesTScore | ItqDichotomousScore | Pcl5Score | Dass21Score | GSEScore | None = score_questionnaire_response(responses, sub.questionnaire.name)

      formatted_submissions.append({
        "id": sub.pk,
        "form": form_name, 
        "submission_date": sub.submitted_at, 
        "results": create_questionnaire_result_string(score) if score else "",
        "scheduled_deletion": sub.submitted_at.replace(year = deletion_year, month=deletion_month, day=deletion_day)
      })

      for sub in formatted_submissions:
        if sub['form'] not in unique_form_names:
          unique_form_names.append(sub['form'])


    return {
        'nav_section': 'clients',
        'client_id': client_id, 
        'client_tags': client_basic_information.tags, 
        'screening': client_basic_information.screening_date, 
        'pre_intervention_measures': client_basic_information.pre_intervention_measures_date, 
        'post_intervention_measures': client_basic_information.post_intervention_measures_date, 
        'feedback_form':client_basic_information.feedback_form_date, 
        'access_renewed_date': access_renewed_date, 
        'access_expiry_date': access_expiry_date, 
        'access_status': access_status,
        'submissions': formatted_submissions, 
        'form_submissions_filter_options': unique_form_names
      }
  except Client.DoesNotExist:
    return {
      'nav_section': 'clients',
      'client_id': client_id, 
      'client_tags': [], 
      'screening': None, 
      'pre_intervention_measures': None, 
      'post_intervention_measures': None, 
      'feedback_form': None, 
      'access_renewed_date': None, 
      'access_expiry_date': None, 
      'access_status': "Client Not Found",
      'submissions': [], 
      'form_submissions_filter_options': []
    }
