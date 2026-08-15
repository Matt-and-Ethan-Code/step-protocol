from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url
from step_solo.util.identified import require_identified


def step_solo_introduction(req: HttpRequest) -> HttpResponse:
    (client_id, provider_email) = require_identified(req)
    ctx = {
        "title": "STEP Solo Introduction",
        "video_url": get_video_url('solo_introduction')
    }
    return render(req, 'step_solo/step_solo_introduction.html', context=ctx)
