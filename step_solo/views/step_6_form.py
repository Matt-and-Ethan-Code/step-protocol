from django.http import HttpRequest, HttpResponse
from step_solo.util.solo_form import solo_form
from step_solo.util.identified import solo_session_required
from step_solo.util.form_tokens import STEP_6_TOKEN

@solo_session_required()
def step_6_form(request: HttpRequest) -> HttpResponse:
    return solo_form(request, STEP_6_TOKEN, 'step_solo/step_6_form.html', 'STEP 6', 'solo_step_6_form', 'solo_step_6', 'solo_worksheet_upload')
