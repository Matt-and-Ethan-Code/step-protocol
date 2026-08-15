from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
import clinician_overview.util.client
import clinician_overview.util.access
from step_solo.util import identified

def index(req: HttpRequest) -> HttpResponse:
    if req.POST:
        return index_submit(req)
    else:
        return index_get(req)
    
def index_get(req: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "STEP Solo",
        "error": None,
    }
    return render(req, 'step_solo/index.html', context=ctx)

def index_submit(req: HttpRequest) -> HttpResponse:
    client_id = req.POST.get('client_id', None)
    if client_id is None or len(client_id.strip()) == 0: return HttpResponseBadRequest("Bad client_id")
    client_id = client_id.strip()

    provider_email = req.POST.get('provider_email', None)
    if provider_email is None: return HttpResponseBadRequest("Bad provider_email")

    # check that client id exists
    client = clinician_overview.util.client.find(client_id, provider_email)
    if client is None:
        ctx = {
            "title": "STEP Solo",
            "error": "not_found",
            "client_id": client_id,
            "provider_email": provider_email,
        }
        return render(req, 'step_solo/index.html', context=ctx)
    has_access = clinician_overview.util.access.has_access(client)
    if has_access is None:
        ctx = {
            "title": "STEP Solo",
            "error": "no_access",
            "client_id": client_id,
            "provider_email": provider_email,
        }
        return render(req, 'step_solo/index.html', context=ctx)
    identified.set_identity(req, client_id, provider_email)
    return redirect('solo_what_to_expect')
