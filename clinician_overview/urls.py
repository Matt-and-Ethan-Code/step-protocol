from django.urls import path
from django.http import HttpRequest, HttpResponse
from clinician_overview.views import client_responses_page, measures_page, questionnaire_response_page, not_clinician_page, notifications_page, clients_page, client_summary_page, client_id_route
from django.shortcuts import render, redirect

def handle_index(_req: HttpRequest) -> HttpResponse:
  return redirect('/clinician/notifications')

urlpatterns = [
  path('', handle_index),
  path('notifications', notifications_page, name='notifications'),
  path('clients', clients_page, name='clients'),
  path('measures', measures_page, name='measures'),
  path('clients/<str:client_id>', client_summary_page, name='client_summary'),
  path('response/<str:questionnaire_response_id>', questionnaire_response_page),
  path('clinician-required', not_clinician_page),
  path('esme', lambda r: render(r, 'clinician_overview/clinician_base_layout.html')),
  path('<str:client_id>', client_responses_page),
  path('random-client-id', client_id_route.random_client_id), 
]