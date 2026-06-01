from django.db.models.manager import BaseManager
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Any, TypedDict
from datetime import datetime

from django.utils import timezone
from clinician_overview.models import AccessGrant, Client
from initial_screening.models import QuestionnaireResponse, FormMembership
import calendar

class SubmissionSummary(TypedDict):
    id: int
    form: str
    submission_date: datetime 
    results: str
    scheduled_deletion: datetime

def client_summary_page(request: HttpRequest, client_id: str) -> HttpResponse:
  ctx = make_context(client_id)
  return render(request, 'clinician_overview/client_summary_page.html', context=ctx)

def get_form_completion_date_for_client(client_id: Client, form_id: int)  -> datetime | None:
  last_questionnaire = FormMembership.objects.filter(form_id = form_id).order_by("order").last()
  if last_questionnaire:
    last_response = QuestionnaireResponse.objects.filter(user_identifier=client_id, form_id=form_id, questionnaire_id=last_questionnaire.questionnaire.id).order_by("submitted_at").last()

    if last_response:
      return last_response.submitted_at

def make_context(client_id: str) -> dict[str, Any]:
  try:
    client: Client = Client.objects.get(client_id=client_id)
    client_tags: list[str] = client.tags

    screening_form_id = 1
    feedback_form_id = 2 
    pre_test_form_id = 3
    post_test_form_id = 4 
    unique_form_names: list[str] = []

    screening_date = get_form_completion_date_for_client(client, screening_form_id)
    pre_intervention_date = get_form_completion_date_for_client(client, pre_test_form_id)
    post_intervention_date = get_form_completion_date_for_client(client, post_test_form_id)
    feedback_form_date = get_form_completion_date_for_client(client, feedback_form_id)

    access_grant = AccessGrant.objects.filter(client=client).first()
    if access_grant:
      access_renewed_date = access_grant.created_at
      access_expiry_date = access_grant.expires_at
      access_status = "Expiring Soon" if access_expiry_date > timezone.now() else "Expired"
    else:
      access_renewed_date = None
      access_expiry_date = None
      access_status = "No Access"

    submissions: BaseManager[QuestionnaireResponse] = QuestionnaireResponse.objects.filter(user_identifier = client)

    formatted_submissions: list[SubmissionSummary] = []
    for sub in submissions:
      form_name = f"{sub.form.name}: {sub.questionnaire.name}"

      # calculate deletion date -- 6 months after the submitted date
      deletion_month = sub.submitted_at.month - 1 + 6 
      deletion_year = sub.submitted_at.year + deletion_month // 12 
      deletion_month = deletion_month % 12 + 1
      deletion_day = min(sub.submitted_at.day, calendar.monthrange(deletion_year, deletion_month)[1])

      formatted_submissions.append({
        "id": sub.pk,
        "form": form_name, 
        "submission_date": sub.submitted_at, 
        "results": "", 
        "scheduled_deletion": sub.submitted_at.replace(year = deletion_year, month=deletion_month, day=deletion_day)
      })

      for sub in formatted_submissions:
        if sub['form'] not in unique_form_names:
          unique_form_names.append(sub['form'])

    return {
        'nav_section': 'clients',
        'client_id': client_id, 
        'client_tags': client_tags, 
        'screening': screening_date, 
        'pre_intervention_measures': pre_intervention_date, 
        'post_intervention_measures': post_intervention_date, 
        'feedback_form':feedback_form_date, 
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