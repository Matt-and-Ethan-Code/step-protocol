from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from initial_screening.models import QuestionnaireResponse
from initial_screening.decorators import clinician_required
from typing import Any

"""
TODO
Include/sort when they last submitted
- new column for if it has been viewed or not
  - greyed out/less prominent if it has been viewed
- space for an alarm icon (based on score)
"""

@clinician_required
def clinician_overview_page(request: HttpRequest) -> HttpResponse:
  """
  Show overview of clients that.
  """

  context = clinician_overview_page_context(responded_clients())
  return render(request, "clinician_overview/clinician_overview_page.html", context=context)


def clinician_overview_page_context(client_ids: list[str]) -> dict[str, Any]:
  return {
    "client_ids": client_ids
  }

def responded_clients() -> list[str]:
  """
  Get all client ids of those who have submitted a response
  """
  user_identifier_maps = QuestionnaireResponse.objects.values('user_identifier').distinct()
  user_identifiers: list[str] = []
  for user_identifier_map in user_identifier_maps:
    user_identifier: str = user_identifier_map['user_identifier']
    user_identifiers.append(user_identifier)
  return user_identifiers