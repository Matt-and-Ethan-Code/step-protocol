from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from step_solo.util.get_video_url import get_video_url

from .forms import AgreementForm
from .models import Agreement, ProviderConfirmation


def step_together_portal_view(request: HttpRequest) -> HttpResponse:
    return render(request, "step_together/step-together.html", {
        "nav_section": "step-together"
    })

def step_together_manual(request: HttpRequest) -> HttpResponse:
    return render(request, "step_together/step-together-manual.html", {
        "nav_section": "step-together"
    })

def step_together_pregroup_checklist(request: HttpRequest) -> HttpResponse:
    return render(request, "step_together/step-together-pre-group-checklist.html", {
        "nav_section": "step-together"
    })

def welcome_to_step_together(request: HttpRequest) -> HttpResponse:
    return render(request, "step_together/welcome-to-step-together.html", {
        "nav_section": "step-together"
    })

def self_care_introduction(request:HttpRequest) -> HttpResponse:
    return render(request, "step_together/self-care-introduction.html", {
        "nav_section": "step-together", 
        "video_url": get_video_url('st_self_care_introduction')
    })

def bilateral_tapping(request:HttpRequest) -> HttpResponse: 
    return render(request, 'step_together/bilateral-tapping.html', {
        'nav_section': 'step-together', 
        'video_url': get_video_url('st_bilateral_tapping')
    })


def agreement_view(request: HttpRequest) -> HttpResponse:
    agreement = get_object_or_404(Agreement, current=True)

    if request.method == "POST":
        form = AgreementForm(request.POST, agreement=agreement)
        if form.is_valid():
            # by convention the first text question is the provider's name
            # and the second is their organization (see ProviderConfirmation)
            answers = form.get_text_answers()
            provider_name = answers[0] if len(answers) > 0 else ""
            provider_organization = answers[1] if len(answers) > 1 else ""

            ProviderConfirmation.objects.create(
                provider_name=provider_name,
                provider_organization=provider_organization,
                agreement=agreement,
            )
            return redirect("notifications")  
    else:
        form = AgreementForm(agreement=agreement)

    return render(request, "step_together/agreement.html", {
        "form": form,
        "agreement": agreement,
    })
