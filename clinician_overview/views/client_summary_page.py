from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Any
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from clinician_overview.models import AccessGrant, Client
from clinician_overview.util import client as clientm
from clinician_overview.util import access
from initial_screening.models import QuestionnaireResponse, FormMembership
from datetime import date
import calendar
from typing import cast


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

def make_context(client: Client, maybe_access_grant: AccessGrant | None) -> dict[str, Any]:
  try:
    client_tags: list[str] = client.tags

    screening_form_id = 1
    feedback_form_id = 2 
    pre_test_form_id = 3
    post_test_form_id = 4 

    screening_date = get_form_completion_date_for_client(client, screening_form_id)
    pre_intervention_date = get_form_completion_date_for_client(client, pre_test_form_id)
    post_intervention_date = get_form_completion_date_for_client(client, post_test_form_id)
    feedback_form_date = get_form_completion_date_for_client(client, feedback_form_id)

    access_renewed_date: datetime| None = None
    access_expiry_date: datetime | None = None
    access_status: str = ""
    if maybe_access_grant:
      access_grant: AccessGrant = maybe_access_grant
      access_renewed_date = access_grant.created_at
      access_expiry_date = access_grant.expires_at
      access_status = "Expiring Soon" if access_expiry_date and access_expiry_date > timezone.now() else "Expired"
    else:
      access_renewed_date = None
      access_expiry_date = None
      access_status = "No Access"

    submissions = QuestionnaireResponse.objects.filter(user_identifier = client)

    formatted_submissions: list[Any] = []
    for sub in submissions:
      form_name = f"{sub.form.name}: {sub.questionnaire.name}"

      # calculate deletion date -- 6 months after the submitted date
      deletion_month = sub.submitted_at.month - 1 + 6 
      deletion_year = sub.submitted_at.year + deletion_month // 12 
      deletion_month = deletion_month % 12 + 1
      deletion_day = min(sub.submitted_at.day, calendar.monthrange(deletion_year, deletion_month)[1])

      formatted_submissions.append({
        "form": form_name, 
        "submission_date": sub.submitted_at, 
        "results": "", 
        "scheduled_deletion": sub.submitted_at.replace(year = deletion_year, month=deletion_month, day=deletion_day)
      })


    return {
      'nav_section': 'clients',
      'client_id': client.client_id,
      'client_tags': client_tags, 
      'screening': screening_date, 
      'pre_intervention_measures': pre_intervention_date, 
      'post_intervention_measures': post_intervention_date, 
      'feedback_form':feedback_form_date, 
      'access_renewed_date': access_renewed_date, 
      'access_expiry_date': access_expiry_date, 
      'access_status': access_status,
      'submissions': formatted_submissions
    }


  except:
    pass
  return {
    'nav_section': 'clients',
    'client_id': client_id, 
    'client_tags': ["Feb 2026", "Mar 2026"], 
    'screening': date(2026, 1, 10), 
    'pre_intervention_measures': date(2026, 1, 11), 
    'post_intervention_measures': None, 
    'feedback_form': None, 
    'access_renewed_date': date(2026, 1, 10), 
    'access_expiry_date': date(2026, 1, 25), 
    'access_status': "Expiring Soon",
    'submissions': [
      {
        'id': 0,
        'form': 'Post-Intervention GSE', 
        'submission_date': date(2026, 1, 9), 
        'results': "Elevated - Priority Review", 
        'scheduled_deletion': date(2026, 1, 19)
      }, 
      {
        'id': 1,
        'form': 'Post-Intervention DASS-21', 
        'submission_date': date(2026, 1, 10), 
        'results': "Within Range - Routine Review", 
        'scheduled_deletion': date(2026, 1, 19)
      }
    ], 
    'form_submissions_filter_options': ['Post-Intervention DASS-21', 'Post-Intervention GSE']
  }
