from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from step_solo.util.identified import require_identified



def self_regulation_strategies(req: HttpRequest) -> HttpResponse:
    (client_id, provider_email) = require_identified(req)
    ctx = {
        "title": "Self-Regulation Strategies"
    }
    return render(req, 'step_solo/self_regulation_strategies.html', context=ctx)
