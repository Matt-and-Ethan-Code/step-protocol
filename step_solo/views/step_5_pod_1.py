from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.identified import solo_session_required


@solo_session_required()
def step_5_pod_1(request: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "STEP 5 - PoD 1",
        "previous_url": "solo_step_2",
        "next_url": "solo_step_5_pod_1_form"
    }
    return render(request, 'step_solo/step_5_pod1.html', context=ctx)
