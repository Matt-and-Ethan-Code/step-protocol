from django.shortcuts import render
from django.http import HttpRequest

from provider_intake.forms import ProviderIntakeForm
#from .forms import ProviderIntakeForm

def provider_intake(request: HttpRequest):
    if request.method == "POST":
        pass
    else: 
        form = ProviderIntakeForm()
        return render(request, "provider_intake/provider_questionnaire.html", {
            "form": form
        })