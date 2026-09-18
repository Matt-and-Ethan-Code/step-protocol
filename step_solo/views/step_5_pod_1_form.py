from django.http import HttpRequest, HttpResponse
from step_solo.util.solo_form import solo_form
from step_solo.util.identified import solo_session_required
from step_solo.util.form_tokens import STEP_5_POD_1_TOKEN

@solo_session_required()
def step_5_pod_1_form(request: HttpRequest) -> HttpResponse:
    return solo_form(request, STEP_5_POD_1_TOKEN, 'step_solo/step_5_pod1_form.html', 'STEP 5 - PoD 1', 'solo_step_5_pod_1_form', 'solo_step_5_pod_1', 'solo_step_5_pod_1_last_form',)
