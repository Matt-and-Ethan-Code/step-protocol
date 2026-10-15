from django.http import HttpRequest, HttpResponse
from step_solo.util.identified import solo_session_required
from step_solo.util.form_tokens import STEP_2_TOKEN
from step_solo.util.solo_form import solo_form


@solo_session_required()
def step_2(request: HttpRequest) -> HttpResponse:
    return solo_form(request, STEP_2_TOKEN, 'step_solo/step_2.html', 'STEP 2', 'solo_step_2', 'solo_sheet_review', 'solo_step_5_pod_1')
