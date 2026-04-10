from django.http import HttpRequest, HttpResponse, JsonResponse
import clinician_overview.util.client_id as client_id

def random_client_id(req: HttpRequest) -> HttpResponse:
  payload = {
    "client_id": client_id.generate()
  }
  return JsonResponse(payload)