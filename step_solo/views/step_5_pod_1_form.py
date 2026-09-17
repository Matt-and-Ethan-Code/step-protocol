from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from step_solo.util.levels import with_levels
from step_solo.util.solo_form import solo_form


STEP_5_POD_1_TOKEN = "solo_step_5_pod_1"
def step_5_pod_1_form(request: HttpRequest) -> HttpResponse:
    return solo_form(request, STEP_5_POD_1_TOKEN, 'step_solo/step_5_pod1_form.html', 'STEP 5 - POD 1', 'solo_step_5_pod_1_form', 'solo_step_5_pod_1', 'solo_step_5_pod_1_last_form',)
