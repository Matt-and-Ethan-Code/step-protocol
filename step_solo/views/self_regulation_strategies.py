from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from step_solo.util.identified import solo_session_required


@solo_session_required()
def self_regulation_strategies(req: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "Self-Regulation Strategies",
        "previous_url": "solo_what_to_expect",
        "next_url": "solo_introduction",
        
    }
    return render(req, 'step_solo/self_regulation_strategies.html', context=ctx)
