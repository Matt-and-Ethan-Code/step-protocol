from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.identified import require_identified

def getting_started(req: HttpRequest) -> HttpResponse:
    (client_id, provider_email) = require_identified(req)
    ctx = {}
    return render(req, 'step_solo/getting_started.html', context=ctx)
