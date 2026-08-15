from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.identified import require_identified


def pre_check_in(req: HttpRequest) -> HttpResponse:
    (client_id, provider_email) = require_identified(req)
    ctx={}
    return render(req, 'step_solo/pre_check_in.html', context=ctx)
