from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.identified import solo_session_required

@solo_session_required()
def getting_started(req: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "Getting Started",
        "previous_url": "solo_introduction",
        "next_url": "solo_bilateral_tapping"
    }
    return render(req, 'step_solo/getting_started.html', context=ctx)
