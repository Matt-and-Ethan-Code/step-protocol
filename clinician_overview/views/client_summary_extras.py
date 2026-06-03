from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from typing import cast
from clinician_overview.util import access, client as clientm


@require_POST
@login_required
def revoke_access(request: HttpRequest) -> HttpResponse:
    query_set = request.POST
    client_id: str | None = query_set.get('client_id')
    if not client_id: return HttpResponseBadRequest()
    user = cast(User, request.user)
    client = clientm.find(client_id, user)
    if not client: return HttpResponseNotFound(f"{client_id=} not found!")
    
    access.revoke_current_access_for(user, client)
    
    
    return redirect(f"/clinician/clients/{client_id}")
