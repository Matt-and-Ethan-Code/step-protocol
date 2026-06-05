from django.urls import path
from django.http import HttpRequest, HttpResponse
from clinician_overview.views import delete_clients_route, delete_responses_route, client_responses_page, save_tags_route, measures_page, questionnaire_response_page, not_clinician_page, notifications_page, clients_page, client_summary_page, client_id_route, export_csv_route
from django.shortcuts import redirect

def handle_index(_req: HttpRequest) -> HttpResponse:
  return redirect('/clinician/notifications')

urlpatterns = [
  path('', handle_index),
  path('random-client-id', client_id_route.random_client_id, name='get_random_id'),
  path('create-client-id', client_id_route.create_client_id, name='create_client_id'),
  path('notifications', notifications_page, name='notifications'),
  path('clients', clients_page, name='clients'),
  path('measures', measures_page, name='measures'),
  path('clients/<str:client_id>/response/<str:questionnaire_response_id>', questionnaire_response_page),
  path('clients/<str:client_id>/save-tags', save_tags_route, name='save_tags'),
  path('clients/<str:client_id>/export', export_csv_route,name="export"),
  path('clients/<str:client_id>/delete-submissions', delete_responses_route),
  path('clients/delete-clients', delete_clients_route, name='delete_clients'),
  path('clients/<str:client_id>', client_summary_page, name='client_summary'),
  path('clinician-required', not_clinician_page),
  path('<str:client_id>', client_responses_page),
  
]