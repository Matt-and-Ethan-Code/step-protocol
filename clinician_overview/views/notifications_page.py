from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from dataclasses import dataclass
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.decorators import login_required
from clinician_overview.models import Client
from initial_screening.models import FormMembership, QuestionnaireResponse
#from initial_screening.models import QuestionnaireResponse

@dataclass
class ViewNotification:
  client_id: str
  message: str
  submitted_at: datetime

@login_required
def notifications_page(req: HttpRequest) -> HttpResponse:
  assert isinstance(req.user, AbstractBaseUser)
  submissions = get_submissions(req.user)
  ctx = make_context(submissions)
  return render(req, 'clinician_overview/notifications_page.html', context=ctx)

def get_submissions(user: AbstractBaseUser) -> list[ViewNotification]: 
  # get all clients for this user
  clients = Client.objects.filter(clinician=user)
  notifications: list[ViewNotification] = []
  for client in clients:
    # get all responses where the client selected this clinician
    responses = QuestionnaireResponse.objects.filter(user_identifier=client)

    for response in responses:
      # iterate through all the responses for this client, creating notifications only when it's the last questionnaire in the form
      # note: for us, "submitting the last questionnaire in the form" and "submitting the form" can be treated the same

      # check the last questionnaire for this particular form
      # Note: order_by sorts in ascending order by default, so to get the largest order (latest form), get .last()
      last_questionnaire_in_form = FormMembership.objects.filter(form_id =  response.form.id).order_by("order").last()
      # only create a notification for this response if the questionnaire is the final questionnaire
      if (last_questionnaire_in_form and response.questionnaire.id == last_questionnaire_in_form.questionnaire.id):
        notifications.append(ViewNotification(client.client_id, "Submitted " + response.form.name, response.submitted_at))
  return notifications

def make_context(notifications: list[ViewNotification]) -> dict[str, list[ViewNotification] | str]:
  return {
    "nav_section": "notifications", 
    "notifications": notifications
  }

def mock_messages() -> list[ViewNotification]:
  return [
    ViewNotification("sakf2049", "This thing was submitted", datetime.now()),
    ViewNotification("fkal3058", "This thing was submitted", datetime.now()),
    ViewNotification("slfo2950", "This thing was submitted", datetime.now()),
  ]
