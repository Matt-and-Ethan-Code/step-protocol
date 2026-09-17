from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from step_solo.util.levels import with_levels
from step_solo.util.solo_form import solo_form


STEP_2_TOKEN = "solo_step_2"
def step_2(request: HttpRequest) -> HttpResponse:
    return solo_form(request, STEP_2_TOKEN, 'step_solo/step_2.html', 'STEP 2', 'solo_step_2', 'solo_sheet_review', 'solo_step_5_pod_1')
