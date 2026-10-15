from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url
from step_solo.util.identified import solo_session_required

@solo_session_required()
def solo_8p2(request: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "Solo 8 Part 2",
        "video_url": get_video_url('solo_8p2'),
        "previous_url": "solo_8p1",
        "next_url": "solo_9",
    }
    return render(request, "step_solo/solo_8p2.html", context=ctx)
