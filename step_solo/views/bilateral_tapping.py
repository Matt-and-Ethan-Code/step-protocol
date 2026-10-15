from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url
from step_solo.util.identified import solo_session_required


@solo_session_required()
def bilateral_tapping(req: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "Bilateral Tapping",
        "video_url": get_video_url('bilateral_tapping'),
        "previous_url": "solo_getting_started",
        "next_url": "solo_pre_check_in",
    }
    return render(req, "step_solo/bilateral_tapping.html", context=ctx)
