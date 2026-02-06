from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from typing import Any
from initial_screening.models import QuestionnaireResponse
from initial_screening.decorators import clinician_required

@clinician_required
def questionnaire_response_page(request: HttpRequest, questionnaire_response_id: str) -> HttpResponse:
  questionnaire_response = get_object_or_404(QuestionnaireResponse, id=questionnaire_response_id)

  try:
    context = questionnaire_response_page_context()
    return render(request, 'clinician_overview/client_response_page.html', context=context)
  finally:
    questionnaire_response.view_count += 1
    questionnaire_response.save()

def questionnaire_response_page_context() -> dict[str, Any]:
  return {}

