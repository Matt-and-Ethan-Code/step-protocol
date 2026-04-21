from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Any
from datetime import date

def client_summary_page(request: HttpRequest, client_id: str) -> HttpResponse:
  ctx = make_context(client_id)
  return render(request, 'clinician_overview/client_summary_page.html', context=ctx)

def make_context(client_id: str) -> dict[str, Any]:
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