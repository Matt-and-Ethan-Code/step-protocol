from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from initial_screening.models import QuestionnaireResponse
from typing import Any

@login_required

def clinician_overview_page(request: HttpRequest) -> HttpResponse:
  """
  Show overview of clients that.
  """
  if not user_is_clinician(request.user):
    return render(request, 'clinician_overview/not_clinician_page.html')

  context = clinician_overview_page_context(responded_clients())
  return render(request, "clinician_overview/clinician_overview_page.html", context=context)

def user_is_clinician(user: User): return True

def clinician_overview_page_context(client_ids: list[str]) -> dict[str, Any]:
  return {
    "client_ids": client_ids
  }

def responded_clients() -> list[str]:
  """
  Get all client ids of those who have submitted a response
  """
  user_identifier_maps = QuestionnaireResponse.objects.values('user_identifier').distinct()
  user_identifiers = []
  for user_identifier_map in user_identifier_maps:
    user_identifiers.append(user_identifier_map['user_identifier'])
  return user_identifiers