from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Any
from datetime import date
from clinician_overview.models import ClientId
from initial_screening.models import QuestionnaireResponse
from datetime import date
import calendar

def client_summary_page(request: HttpRequest, client_id: str) -> HttpResponse:
  ctx = make_context(client_id)
  return render(request, 'clinician_overview/client_summary_page.html', context=ctx)

def make_context(client_id: str) -> dict[str, Any]:
  try:
    client: ClientId = ClientId.objects.get(client_id=client_id)
    client_tags: list[str] = client.tags

    # dates -- if done, give date, else, give in progress, else give "not started"

    # screening date -- date the 
    screening_date = None
    pre_intervention_date = None
    post_intervention_date = None 
    feedback_form_date = None 
    
    access_renewed_date = None 
    access_expiry_date = None 
    access_status = "Expiring Soon" 

    submissions = QuestionnaireResponse.objects.filter(user_identifier = client)


    formatted_submissions: list[Any] = []
    for sub in submissions:
      form_name = sub.questionnaire

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
      'client_id': client_id, 
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