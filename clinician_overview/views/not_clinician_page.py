from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def not_clinician_page(request: HttpRequest) -> HttpResponse:
  return render(request, 'clinician_overview/not_clinician_page.html')