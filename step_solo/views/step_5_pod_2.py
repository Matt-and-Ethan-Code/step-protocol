from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.identified import solo_session_required


@solo_session_required()
def step_5_pod_2(request: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "STEP 5 - PoD 2",
        "previous_url": "solo_step_5_pod_1_last_form",
        "next_url": "solo_step_5_pod_2_form"
    }
    return render(request, 'step_solo/step_5_pod2.html', context=ctx)
