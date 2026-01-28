from django.urls import path
from clinician_overview.views.overview_page import overview_page

urlpatterns = [
  path('', overview_page)
]