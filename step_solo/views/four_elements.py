from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url
from step_solo.util.identified import solo_session_required

@solo_session_required()
def four_elements(req: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "4 Elements",
        "video_url": get_video_url('4_elements_with_music'),
        "previous_url": "solo_pre_check_in",
        "next_url": "solo_stress_before_four_elements",
    }
    return render(req, 'step_solo/four_elements.html', context=ctx)
