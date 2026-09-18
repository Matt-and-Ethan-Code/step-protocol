from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def worksheet_upload(request: HttpRequest) -> HttpResponse:
  ctx = {
    "title": "STEP Worksheets",
    "previous_url": "solo_step_6_form",
    "next_url": "solo_container"
  }
  return render(request, "step_solo/worksheet_upload.html", context=ctx)