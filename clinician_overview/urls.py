from django.urls import path
from clinician_overview.views.overview_page import overview_page

urlpatterns = [
  path('<str:client_id>', overview_page)
]