from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Provider
from django.contrib.auth.decorators import login_required
from typing import cast
from django.contrib.auth.models import User

from provider_intake.forms import ProviderIntakeForm

def provider_success(request: HttpRequest) -> HttpResponse:
    return render(request, "provider_intake/provider_success.html")

@login_required
def provider_intake(request: HttpRequest):
    if request.method == "POST":
        user = cast(User, request.user)
        provider = getattr(user, "provider", None)
        form = ProviderIntakeForm(request.POST or None, instance=provider)
        
        if form.is_valid():
            provider: Provider | None = form.save(commit=False)
            if provider:
                provider.user = user
                provider.save()
            return redirect("provider_success")
    else: 
        form = ProviderIntakeForm()
    
    return render(request, "provider_intake/provider_questionnaire.html", {
            "form": form
        })