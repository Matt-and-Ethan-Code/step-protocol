from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
import django.forms as forms
import clinician_overview.util.client_id as client_id
from clinician_overview.models import ClientId
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def random_client_id(req: HttpRequest) -> HttpResponse:
  payload = {
    "client_id": client_id.new_id()
  }
  return JsonResponse(payload)

class NewClientIdForm(forms.Form):
  new_client_id = forms.CharField(label="New Id", max_length=client_id.LENGTH)

#@require_POST
#@login_required
def create_client_id(req: HttpRequest) -> HttpResponse:
  query_set = req.POST
  requested_new_client_id = query_set.get('new_client_id')

  if requested_new_client_id is None:
    return HttpResponseBadRequest() # 405
  
  assert type(requested_new_client_id) == str

  if not client_id.is_valid(requested_new_client_id) or client_id.client_id_exists(requested_new_client_id):
    return HttpResponseBadRequest() # 405
  
  User = get_user_model()
  user = User.objects.order_by('?').first()
  # insert the new id
  new_client_id = ClientId(client_id=requested_new_client_id, clinician=user ,is_active=True)
  new_client_id.save()


  return redirect('/clinician/clients')