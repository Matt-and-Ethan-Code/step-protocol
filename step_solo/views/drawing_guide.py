from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url
from step_solo.util.identified import solo_session_required

@solo_session_required()
def drawing_guide(request: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "Drawing Guide",
        "video_url": get_video_url('drawing_guide'),
        "previous_url": "solo_1",
        "next_url": "solo_2",
    }
    return render(request, "step_solo/drawing_guide.html", context=ctx)
