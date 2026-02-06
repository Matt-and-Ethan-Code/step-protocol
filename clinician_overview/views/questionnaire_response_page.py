from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from typing import Any
from initial_screening.models import QuestionnaireResponse

@login_required
def questionnaire_response_page(request: HttpRequest, questionnaire_response_id: str) -> HttpResponse:
  if not user_is_clinician(request.user):
    return render(request, 'clinicain_overview/not_clinician_page.html')
  questionnaire_response = get_object_or_404(QuestionnaireResponse, id=questionnaire_response_id)
  
  context = questionnaire_response_page_context()
  return render(request, 'clinician_overview/client_response_page.html', context=context)

def user_is_clinician(user: User): return True

def questionnaire_response_page_context() -> dict[str, Any]:
  return {}

