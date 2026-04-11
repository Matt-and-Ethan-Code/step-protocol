from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from dataclasses import dataclass
from datetime import date
def clients_page(req: HttpRequest) -> HttpResponse:
  ctx = make_context(mock_client_infos())
  return render(req, 'clinician_overview/clients_page.html', context=ctx)


@dataclass
class ViewClientInfo:
  client_id: str
  client_id_url: str
  tags: list[str]
  screening_date: date | None
  pre_intervention_measures_date: date | None
  post_intervention_measures_date: date | None
  feedback_form_date: date | None

def make_context(client_infos: list[ViewClientInfo]) -> dict[str, str | list[ViewClientInfo]]:
  return {
    "nav_section": "clients",
    "client_infos": client_infos
  }

def mock_client_infos() -> list[ViewClientInfo]:
  return [
    ViewClientInfo('raspberry raspberry', 'raspberry-raspberry',['feb 2026'], date.today(), None, None, None),
    ViewClientInfo('watery baseball', 'raspberry-raspberry', [], date.today(), None, date.today(), None),
  ]