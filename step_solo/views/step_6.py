from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.identified import solo_session_required


@solo_session_required()
def step_6(request: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "STEP 6",
        "previous_url": "solo_step_5_pod_3_last_form",
        "next_url": "solo_step_6_form"
    }
    return render(request, 'step_solo/step_6.html', context=ctx)
