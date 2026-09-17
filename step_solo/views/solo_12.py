from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url
from step_solo.util.identified import solo_session_required

@solo_session_required()
def solo_12(request: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "Solo 12",
        "video_url": get_video_url('solo_12'),
        "previous_url": "solo_11",
        "next_url": "solo_sheet_review",
    }
    return render(request, "step_solo/solo_12.html", context=ctx)
