from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
import datetime
from django.utils import timezone
import django.forms as forms
from typing import cast
from clinician_overview.util.access import new_grant_until
import clinician_overview.util.client_id as client_id
from clinician_overview.models import Client
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def random_client_id(req: HttpRequest) -> HttpResponse:
  payload = {
    "client_id": client_id.new_id()
  }
  return JsonResponse(payload)

class NewClientIdForm(forms.Form):
  new_client_id = forms.CharField(label="New Id", max_length=client_id.LENGTH)

@require_POST
@login_required
def create_client_id(req: HttpRequest) -> HttpResponse:
  query_set = req.POST
  requested_new_client_id: str | None = query_set.get('new_client_id')

  if requested_new_client_id is None:
    return HttpResponseBadRequest() # 405

  duration_in_days_str: str | None = query_set.get('duration')
  if duration_in_days_str is None: return HttpResponseBadRequest()

  try:
    duration_in_days: int = int(duration_in_days_str)
  except ValueError:
    return HttpResponseBadRequest("duration must be int")

  if duration_in_days <= 0: return HttpResponseBadRequest()
  

  if not client_id.is_valid(requested_new_client_id) or client_id.find(requested_new_client_id):
    return HttpResponseBadRequest() # 405
  

  user = cast(User, req.user)
  # insert the new id
  new_client_id = Client(client_id=requested_new_client_id, clinician=user ,is_active=True)
  new_client_id.save()

  end_date = datetime.timedelta(days=duration_in_days) + timezone.now()
  access_grant = new_grant_until(clinician=user, client=new_client_id, end_date=end_date)
  access_grant.save()

  return redirect('/clinician/clients')
