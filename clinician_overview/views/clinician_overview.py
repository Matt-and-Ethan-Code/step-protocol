from django.http import HttpRequest, HttpResponse
from initial_screening.models import ResponseItem

def clinician_overview_page(request: HttpRequest) -> HttpResponse:
  """
  Show overview of clients.
  """
  return HttpResponse("this is my response!")


def clients():
  