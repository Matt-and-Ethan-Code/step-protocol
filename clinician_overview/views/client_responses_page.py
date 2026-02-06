from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from initial_screening.models import QuestionnaireResponse
from dataclasses import dataclass
from typing import Any, cast


# Create your views here.
@login_required
def client_responses_page(request: HttpRequest, client_id: str) -> HttpResponse:
  user = cast(User, request.user)
  if not user_is_clinician(user):
    return not_clinician(request)
  

  context: dict[str, Any] = overview_page_context(client_id, client_responses(client_id))

  return render(request, "clinician_overview/client_responses_page.html", context=context)


def not_clinician(request: HttpRequest) -> HttpResponse:
  return render(request, "clinician_overview/not_clinician_page.html")

def user_is_clinician(user_email: User):
  clincian_emails = [
    
  ]
  return True
  return user_email in clincian_emails

def client_responses(client_id: str) -> list[QuestionnaireResponse]:
  questionnaire_responses_for_user = QuestionnaireResponse.objects.filter(user_identifier=client_id).order_by('-submitted_at').all()
  return list(questionnaire_responses_for_user)


@dataclass
class ViewQuestionnaireResponse:
  questionnaire_response_id: str
  submitted_at: datetime
  questionnaire_name: str

def overview_page_context(client_id: str, responses: list[QuestionnaireResponse]) -> dict[str, Any]:
  view_responses: list[ViewQuestionnaireResponse] = []
  for response in responses:
    id = str(response.id)
    view_responses.append(ViewQuestionnaireResponse(
      questionnaire_response_id=id,
      submitted_at=response.submitted_at,
      questionnaire_name=response.questionnaire.name
    ))
    
  return {
    'client_id': client_id,
    'responses': view_responses,
  }
  