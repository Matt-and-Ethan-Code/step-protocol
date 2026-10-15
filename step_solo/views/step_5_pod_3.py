from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.identified import solo_session_required


@solo_session_required()
def step_5_pod_3(request: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "STEP 5 - PoD 3",
        "previous_url": "solo_step_5_pod_2_last_form",
        "next_url": "solo_step_5_pod_3_form"
    }
    return render(request, 'step_solo/step_5_pod3.html', context=ctx)
