from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Any

def client_summary_page(request: HttpRequest, client_id: str) -> HttpResponse:
  ctx = make_context(client_id)
  return render(request, 'clinician_overview/client_summary_page.html', context=ctx)

def make_context(client_id: str) -> dict[str, Any]:
  return {
    'nav_section': 'clients',
    'client_id': client_id, 
    'client_tags': ["Feb 2026", "Mar 2026"]
  }