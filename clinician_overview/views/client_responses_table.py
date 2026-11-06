from django.db.models.manager import BaseManager
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from typing import Any
from clinician_overview.util import score_questionnaire_response
from clinician_overview.util.print import render_to_pdf
from clinician_overview.views import metrics_display_string
from clinician_overview.views.questionnaire_response_page import questionnaire_response_page_context
from initial_screening.models import QuestionnaireResponse, ResponseItem
from initial_screening.decorators import clinician_required
from clinician_overview.scoring import *
from django.contrib.auth.decorators import login_required

@clinician_required
@login_required
def client_responses_table(request: HttpRequest, client_id:str, questionnaire_response_id: str) -> HttpResponse:
  questionnaire_response = get_object_or_404(QuestionnaireResponse, id=questionnaire_response_id)
  try:
    context = questionnaire_response_page_context(client_id, questionnaire_response)
    return render(request, 'clinician_overview/client_responses_table.html', context=context)
  finally:
    questionnaire_response.view_count += 1
    questionnaire_response.save()