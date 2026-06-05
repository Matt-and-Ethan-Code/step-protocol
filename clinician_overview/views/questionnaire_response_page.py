from django.db.models.manager import BaseManager
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from typing import Any
from clinician_overview.util import score_questionnaire_response
from clinician_overview.views import metrics_display_string
from initial_screening.models import QuestionnaireResponse, ResponseItem
from initial_screening.decorators import clinician_required
from clinician_overview.scoring import *
from django.contrib.auth.decorators import login_required


@clinician_required
@login_required
def questionnaire_response_page(request: HttpRequest, client_id:str, questionnaire_response_id: str) -> HttpResponse:
  questionnaire_response = get_object_or_404(QuestionnaireResponse, id=questionnaire_response_id)
  try:
    context = questionnaire_response_page_context(client_id, questionnaire_response)
    return render(request, 'clinician_overview/client_response_page.html', context=context)
  finally:
    questionnaire_response.view_count += 1
    questionnaire_response.save()

def questionnaire_response_page_context(client_id: str, questionnaire_response: QuestionnaireResponse) -> dict[str, Any]:
  submitted_date = questionnaire_response.submitted_at
  questionnaire_title = questionnaire_response.questionnaire.name

  responseItems: BaseManager[ResponseItem] = ResponseItem.objects.filter(response = questionnaire_response).order_by("question__order")

  questionnaire_explanation_content: str = ""
  questionnaire_score = score_questionnaire_response.score_questionnaire_response(responseItems, questionnaire_title)
  if "DES-T" in questionnaire_title and isinstance(questionnaire_score, DesTScore):
    questionnaire_explanation_content: str = metrics_display_string.render_dest(questionnaire_score)
  elif "ITQ" in questionnaire_title and isinstance(questionnaire_score, ItqDichotomousScore):
    questionnaire_explanation_content: str = metrics_display_string.render_itq(questionnaire_score)
  elif "PCL-5" in questionnaire_title and isinstance(questionnaire_score, Pcl5Score):
    questionnaire_explanation_content: str = metrics_display_string.render_pcl5(questionnaire_score)
  elif "DASS-21" in questionnaire_title and isinstance(questionnaire_score, Dass21Score):
    questionnaire_explanation_content: str = metrics_display_string.render_dass21(questionnaire_score)
  elif "GSE" in questionnaire_title and isinstance(questionnaire_score, GSEScore):
    questionnaire_explanation_content: str = metrics_display_string.render_gse(questionnaire_score)

  return {
      'nav_section': 'clients',
      'client_id': client_id, 
      "submitted_at": submitted_date,
      "questionnaire_title": questionnaire_title, 
      "html_result_display": questionnaire_explanation_content, 
      "response_items": responseItems
    }

