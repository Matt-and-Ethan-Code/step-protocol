from django.urls import path
from clinician_overview.views import clinician_overview_page, client_responses_page, questionnaire_response_page, not_clinician_page

urlpatterns = [
  path('', clinician_overview_page),
  path('<str:client_id>', client_responses_page),
  path('response/<str:questionnaire_response_id>', questionnaire_response_page),
  path('clinician-required', not_clinician_page)
]