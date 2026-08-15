from django.shortcuts import render
from django.http import HttpRequest, HttpResponse



def self_regulation_strategies(req: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "Self-Regulation Strategies"
    }
    return render(req, 'step_solo/self_regulation_strategies.html', context=ctx)
