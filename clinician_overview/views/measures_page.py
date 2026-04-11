from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from initial_screening.decorators.clinician_decorator import clinician_required

@clinician_required
def measures_page(request: HttpRequest) -> HttpResponse:
    print("routing for measures")
    return render(request, 'clinician_overview/measures_page.html')