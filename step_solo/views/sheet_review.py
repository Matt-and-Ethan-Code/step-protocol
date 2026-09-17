from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url
from step_solo.util.identified import solo_session_required

@solo_session_required()
def sheet_review(request: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "Sheet Review",
        "previous_url": "solo_12",
        "next_url": "solo_step_2",
    }
    return render(request, "step_solo/sheet_review.html", context=ctx)
