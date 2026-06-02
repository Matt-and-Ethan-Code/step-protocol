from clinician_overview.models import Client
from initial_screening.models import FormMembership, QuestionnaireResponse
from typing import Any
from dataclasses import dataclass
from datetime import date, datetime

@dataclass
class ViewClientInfo:
  client_id: str
  tags: list[str]
  screening_date: date | None
  pre_intervention_measures_date: date | None
  post_intervention_measures_date: date | None
  feedback_form_date: date | None

def get_form_completion_date_for_client(client_id: Client, form_id: int)  -> datetime | None:
  last_questionnaire = FormMembership.objects.filter(form_id = form_id).order_by("order").last()
  if last_questionnaire:
    last_response = QuestionnaireResponse.objects.filter(user_identifier=client_id, form_id=form_id, questionnaire_id=last_questionnaire.questionnaire.id).order_by("submitted_at").last()

    if last_response:
      return last_response.submitted_at


def get_client_information(client_id: str) -> Any:
    client: Client = Client.objects.get(client_id=client_id)
    client_tags: list[str] = client.tags

    screening_form_id = 1
    feedback_form_id = 2 
    pre_test_form_id = 3
    post_test_form_id = 4 

    screening_date: datetime | None = get_form_completion_date_for_client(client, screening_form_id)
    pre_intervention_date: datetime | None = get_form_completion_date_for_client(client, pre_test_form_id)
    post_intervention_date: datetime | None = get_form_completion_date_for_client(client, post_test_form_id)
    feedback_form_date: datetime | None = get_form_completion_date_for_client(client, feedback_form_id)

    result_dict: dict[str, Any] = {
        'client_id': client_id, 
        'tags': client_tags, 
        'screening_date': screening_date, 
        'pre_intervention_measures_date': pre_intervention_date, 
        'post_intervention_measures_date': post_intervention_date, 
        'feedback_form_date': feedback_form_date
    }
    return ViewClientInfo(**result_dict)