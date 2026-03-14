from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ViewNotification:
  client_id: str
  message: str
  submitted_at: datetime

def notifications_page(req: HttpRequest) -> HttpResponse:
  ctx = make_context(mock_messages())
  return render(req, 'clinician_overview/notifications_page.html', context=ctx)


def make_context(notifications: list[ViewNotification]):
  return {
    "notifications": notifications
  }

def mock_messages() -> list[ViewNotification]:
  return [
    ViewNotification("rollerblading octopus", "This thing was submitted", datetime.now()),
    ViewNotification("squiggly cactus", "This thing was submitted", datetime.now()),
    ViewNotification("maroon keyboard", "This thing was submitted", datetime.now()),
  ]
