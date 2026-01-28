from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def overview_page(request: HttpRequest) -> HttpResponse:
  context = {}
  return render(request, "clinician_overview/overview_page.html", context=context)


