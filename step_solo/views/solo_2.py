from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url
from step_solo.util.identified import solo_session_required

@solo_session_required()
def solo_2(request: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "Solo 2",
        "video_url": get_video_url('solo_2'),
        "previous_url": "solo_drawing_guide",
        "next_url": "solo_3",
    }
    return render(request, "step_solo/solo_2.html", context=ctx)
