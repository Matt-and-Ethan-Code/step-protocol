from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from step_solo.util.solo_form import solo_form


STEP_5_POD_1_LAST_TOKEN = "solo_step_5_pod_1_last"
def step_5_pod_1_last_form(request: HttpRequest) -> HttpResponse:
    return solo_form(request, STEP_5_POD_1_LAST_TOKEN, 'step_solo/step_5_pod1_last_form.html', 'STEP 5 - POD 1', 'solo_step_5_pod_1_last_form', 'solo_step_5_pod_1_form', 'solo_container',)
