from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from typing import Any
from clinician_overview.models import ClientId
from dataclasses import dataclass
from datetime import date
import clinician_overview.util.client_id as client_id

def clients_page(req: HttpRequest) -> HttpResponse:
  client_ids = ClientId.objects.all()
  client_infos: list[ViewClientInfo] = []
  for id in client_ids:
    client_infos.append(ViewClientInfo(
      client_id=id.client_id,
      client_id_url=id.client_id,
      tags=[],
      screening_date=date.today(),
      pre_intervention_measures_date=None,
      post_intervention_measures_date=None,
      feedback_form_date=None
    ))

  ctx = make_context(client_infos)
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

def make_context(client_infos: list[ViewClientInfo]) -> dict[str, Any]:
  return {
    "client_infos": client_infos,
    "initial_client_id": client_id.new_id()
  }

def mock_client_infos() -> list[ViewClientInfo]:
  return [
    ViewClientInfo('hxto3849', 'hxto3849',['feb 2026'], date.today(), None, None, None),
    ViewClientInfo('ostc0204', 'ostc0204', [], date.today(), None, date.today(), None),
  ]