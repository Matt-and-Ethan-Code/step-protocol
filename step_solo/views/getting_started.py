from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def getting_started(req: HttpRequest) -> HttpResponse:
    ctx = {}
    return render(req, 'step_solo/getting_started.html', context=ctx)
