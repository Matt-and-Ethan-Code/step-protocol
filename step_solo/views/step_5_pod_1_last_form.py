from django.http import HttpRequest, HttpResponse
from step_solo.util.identified import solo_session_required
from step_solo.util.form_tokens import STEP_5_POD_1_LAST_TOKEN
from step_solo.util.solo_form import solo_form

@solo_session_required()
def step_5_pod_1_last_form(request: HttpRequest) -> HttpResponse:
    return solo_form(request, STEP_5_POD_1_LAST_TOKEN, 'step_solo/step_5_pod1_last_form.html', 'STEP 5 - PoD 1', 'solo_step_5_pod_1_last_form', 'solo_step_5_pod_1_form', 'solo_step_5_pod_2',)
