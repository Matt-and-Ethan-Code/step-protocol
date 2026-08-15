from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url
from step_solo.util.identified import require_identified


def bilateral_tapping(req: HttpRequest) -> HttpResponse:
    (client_id, provider_email) = require_identified(req)
    ctx = {
        "video_url": get_video_url('bilateral_tapping')
    }
    return render(req, "step_solo/bilateral_tapping.html", context=ctx)
