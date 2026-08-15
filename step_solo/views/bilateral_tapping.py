from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from step_solo.util.get_video_url import get_video_url


def bilateral_tapping(req: HttpRequest) -> HttpResponse:
    ctx = {
        "video_url": get_video_url('bilateral_tapping')
    }
    return render(req, "step_solo/bilateral_tapping.html", context=ctx)
