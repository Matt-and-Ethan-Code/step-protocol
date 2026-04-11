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
