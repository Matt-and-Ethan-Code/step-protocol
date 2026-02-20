from django.urls import path
from clinician_overview.views import clinician_overview_page, client_responses_page, questionnaire_response_page, not_clinician_page
from django.shortcuts import render
urlpatterns = [
  path('', clinician_overview_page),
  path('response/<str:questionnaire_response_id>', questionnaire_response_page),
  path('clinician-required', not_clinician_page),
  path('esme', lambda r: render(r, 'clinician_overview/clinician_base_layout.html')),
  path('<str:client_id>', client_responses_page),
]