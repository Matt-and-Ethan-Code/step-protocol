from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url
from step_solo.util.identified import solo_session_required

@solo_session_required()
def solo_1(request: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "Solo 1",
        "video_url": get_video_url('solo_1'),
        "previous_url": "solo_stress_after_four_elements",
        "next_url": "solo_drawing_guide",
    }
    return render(request, "step_solo/solo_1.html", context=ctx)
