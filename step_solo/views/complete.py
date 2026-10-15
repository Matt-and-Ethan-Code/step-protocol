from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def complete(request: HttpRequest) -> HttpResponse:
  ctx = {}
  return render(request, "step_solo/complete.html", context=ctx)