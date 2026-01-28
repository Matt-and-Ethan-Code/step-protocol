from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from initial_screening.models import QuestionnaireResponse


# Create your views here.
@login_required
def overview_page(request: HttpRequest) -> HttpResponse:
  user = request.user
  if not user_is_clinician(user):
    return not_clinician()
  context = {}

  return render(request, "clinician_overview/overview_page.html", context=context)


def not_clinician(request: HttpRequest) -> HttpResponse:
  return render(request, "clinician_overview/not_clinician_page.html")

def user_is_clinician(user_email: str):
  clincian_emails = [
    
  ]
  
  return user_email in clincian_emails