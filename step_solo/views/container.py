from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url
from step_solo.util.identified import solo_session_required

@solo_session_required()
def container(request: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "Container",
        "video_url": get_video_url('container_video'),
        "previous_url": "solo_12",
        "next_url": "solo_four_elements_after",
    }
    return render(request, "step_solo/container.html", context=ctx)
