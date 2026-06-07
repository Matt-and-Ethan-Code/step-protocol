from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from clinician_overview.models import Client
from dataclasses import dataclass
from datetime import date
import clinician_overview.util.client as client_id
import clinician_overview.util.get_client_information as get_client_information
from clinician_overview.util.get_client_information import ViewClientInfo
from django.contrib.auth.decorators import login_required
from initial_screening.decorators import clinician_required

@login_required
@clinician_required
def clients_page(req: HttpRequest) -> HttpResponse:
  clients = Client.objects.filter(clinician=req.user)
  client_infos: list[ViewClientInfo] = []
  for client in clients:
    thisClientInfo: ViewClientInfo = get_client_information.get_client_information(client)

    client_infos.append(thisClientInfo)


  ctx = make_context(client_infos)
  return render(req, 'clinician_overview/clients_page.html', context=ctx)


def get_client_infos() -> list[ViewClientInfo]:
  return []

def make_context(client_infos: list[ViewClientInfo]) -> dict[str, str | list[ViewClientInfo]]:
  return {
    "initial_client_id": client_id.new_id(),
    "nav_section": "clients",
    "client_infos": client_infos
  }

