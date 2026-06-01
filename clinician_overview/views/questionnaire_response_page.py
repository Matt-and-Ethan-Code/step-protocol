from django.db.models.manager import BaseManager
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from typing import Any, Callable,  cast
from clinician_overview.views import metrics_display_string
from initial_screening.models import AnswerOption, QuestionnaireResponse, ResponseItem
from initial_screening.decorators import clinician_required
from clinician_overview.scoring import *
import clinician_overview.scoring as scoring

def build_response_form[TResponse, TQuestion](
    response_items: BaseManager[ResponseItem],
    question_indices: range,
    response_mapper: Callable[[int], TResponse],
    question_cast: Callable[[int], TQuestion],
) -> dict[TQuestion, TResponse]:
    response_form: dict[TQuestion, TResponse] = {}
    for i, item in enumerate(response_items):
        #if item.answerID is None or i not in question_indices:
        #   continue

        count = AnswerOption.objects.filter(
            question=item.question,
            order__lt=item.answerID.order if item.answerID is not None else 0
        ).count()
        response_form[question_cast(i)] = response_mapper(count)

    return response_form

@clinician_required
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
  if "DES-T" in questionnaire_title:
    destResponseForm: DesTForm = build_response_form(
      responseItems,
      range(1, 29),
      lambda count: cast(DesTResponse, count * 10),
      lambda i: cast(DesTQuestion, i + 1),
    )

    questionnaire_explanation_content: str = metrics_display_string.render_dest(scoring.dest_score(destResponseForm))
  elif "ITQ" in questionnaire_title: 
    itqResponseForm: ItqForm = build_response_form(
      responseItems,
      range(1, 19),
      lambda count: cast(ItqResponse, count),
      lambda i: cast(ItqQuestion, i),
    )
    questionnaire_explanation_content: str = metrics_display_string.render_itq(scoring.itq_dichotomous_score(itqResponseForm))
  elif "PCL-5" in questionnaire_title:
    pclResponseForm: Pcl5Form = build_response_form(
      responseItems,
      range(1, 21),
      lambda count: cast(Pcl5Response, count),
      lambda i: cast(Pcl5Question, i + 1),
    )
    score = scoring.pcl5_score(pclResponseForm)
    questionnaire_explanation_content: str = metrics_display_string.render_pcl5(score)
  elif "DASS-21" in questionnaire_title:
    dassResponseForm: Dass21Form = build_response_form(
      responseItems,
      range(1, 22),
      lambda count: cast(Dass21Response, count),
      lambda i: cast(Dass21Question, i + 1),
    )
    dass_score: Dass21Score = scoring.dass21_score(dassResponseForm)
    questionnaire_explanation_content: str = metrics_display_string.render_dass21(dass_score)
  elif "GSE" in questionnaire_title:
    gseResponseForm: GSEForm = build_response_form(
      responseItems,
      range(1, 22),
      lambda count: cast(GSEResponse, count),
      lambda i: cast(GSEQuestion, i),
    )
    gse_score: GSEScore = scoring.gse_score(gseResponseForm)
    questionnaire_explanation_content: str = metrics_display_string.render_gse(gse_score)

  
  return {
      'nav_section': 'clients',
      'client_id': client_id, 
      "submitted_at": submitted_date,
      "questionnaire_title": questionnaire_title, 
      "html_result_display": questionnaire_explanation_content, 
      "response_items": responseItems
    }

