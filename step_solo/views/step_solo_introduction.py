from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url
from step_solo.util.identified import solo_session_required

@solo_session_required()
def step_solo_introduction(req: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "STEP Solo Introduction",
        "video_url": get_video_url('solo_introduction'),
        "previous_url": "solo_self_regulation_strategies",
        "next_url": "solo_getting_started"
        
    }
    return render(req, 'step_solo/step_solo_introduction.html', context=ctx)
