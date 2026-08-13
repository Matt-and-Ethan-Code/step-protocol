from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(req: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "STEP Solo"
    }
    return render(req, 'step_solo/index.html', context=ctx)
