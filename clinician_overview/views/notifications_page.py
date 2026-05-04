from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from dataclasses import dataclass
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.decorators import login_required
from clinician_overview.models import ClientId
from initial_screening.models import QuestionnaireResponse
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
  clients = ClientId.objects.filter(clinician=user)
  notifications: list[ViewNotification] = []
  for client in clients:
    responses = QuestionnaireResponse.objects.filter(user_identifier=client)
    for response in responses:
      notifications.append(ViewNotification(client.client_id, "New Submission", response.submitted_at))
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
