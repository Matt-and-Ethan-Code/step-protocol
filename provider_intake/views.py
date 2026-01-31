from django.shortcuts import render
from django.http import HttpRequest

def provider_intake(request: HttpRequest):

    return render(request, "provider_intake/provider_questionnaire.html")