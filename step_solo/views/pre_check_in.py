from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.identified import solo_session_required


@solo_session_required()
def pre_check_in(req: HttpRequest) -> HttpResponse:
    ctx={
        "title": "Check in: Have you Watched The Introduction?",
        "previous_url": "solo_bilateral_tapping",
        "next_url": "solo_four_elements",
    }
    return render(req, 'step_solo/pre_check_in.html', context=ctx)
