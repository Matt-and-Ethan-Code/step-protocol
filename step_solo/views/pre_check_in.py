from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def pre_check_in(req: HttpRequest) -> HttpResponse:
    ctx={}
    return render(req, 'step_solo/pre_check_in.html', context=ctx)
