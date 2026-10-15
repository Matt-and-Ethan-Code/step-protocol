from django.http import HttpRequest, HttpResponse
from step_solo.util.solo_form import solo_form
from step_solo.util.identified import solo_session_required
from step_solo.util.form_tokens import STEP_5_POD_2_TOKEN


@solo_session_required()
def step_5_pod_2_form(request: HttpRequest) -> HttpResponse:
    return solo_form(request, STEP_5_POD_2_TOKEN, 'step_solo/step_5_pod2_form.html', 'STEP 5 - PoD 2', 'solo_step_5_pod_2_form', 'solo_step_5_pod_2', 'solo_step_5_pod_2_last_form')
