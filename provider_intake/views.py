from xmlrpc.client import boolean
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpRequest, HttpResponse
from .models import Provider
from django.contrib.auth.decorators import login_required
from typing import cast
from django.contrib.auth.models import User
from initial_screening.models import Question, AnswerOption
from django.db.models import Max

from provider_intake.forms import ProviderIntakeForm

def provider_success(request: HttpRequest) -> HttpResponse:
    return render(request, "provider_intake/provider_success.html")

def add_provider_answer_option(form: ProviderIntakeForm) -> boolean:
    created = False
    if form.is_valid():
        # add provider as option in the dropdown
        question: Question | Http404 = get_object_or_404(
            Question,
            text="Who is your STEP Intervention Provider?"
        )

        display_text = f"{form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]}"
        internal_value = form.cleaned_data["scoring_email"]

        max_order = question.options.aggregate(
            Max("order")
        )["order__max"] or 0

        answer_option, created = AnswerOption.objects.get_or_create(
            question=question,
            internal_value=internal_value, 
            defaults={
                "text": display_text, 
                "order": max_order + 1
            }
        )

        if created:
            print("Created answer option. ID: ", answer_option.id)

    return created

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

            add_provider_answer_option(form)
            return redirect("provider_success")
        
        return render(request, "provider_intake/provider_questionnaire.html", {
                "form": form
            })
    else: 
        user: User = cast(User, request.user)
        user_email: str = user.email 
        form = ProviderIntakeForm()

        return render(request, "provider_intake/provider_questionnaire.html", {
                "form": form,
                "user_email": user_email
            })
    
