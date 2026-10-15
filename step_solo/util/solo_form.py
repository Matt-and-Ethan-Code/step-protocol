from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from step_solo.util.levels import with_levels


def solo_form(request: HttpRequest, token_name: str, template: str, title: str, self_url: str, prev_url: str, next_url: str) -> HttpResponse:
    if request.POST:
        level = request.POST.get('level', default=None)
        if level is None:
            return redirect(self_url)
        try:
            request.session[token_name] = int(level)
        except ValueError:
            return redirect(self_url)
        return redirect(next_url)
    else:
        existing_level = request.session.get(token_name, default=None)
        ctx = {
            "title": title,
            "preselected_level": str(existing_level),
            "previous_url": prev_url,
            "next_url": next_url,
        }
        return render(request, template, context=with_levels(ctx))
        
    
    
