from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url


def step_solo_introduction(req: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "STEP Solo Introduction",
        "video_url": get_video_url('solo_introduction')
    }
    return render(req, 'step_solo/step_solo_introduction.html', context=ctx)
