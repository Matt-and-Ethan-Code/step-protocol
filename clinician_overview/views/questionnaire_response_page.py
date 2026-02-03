from django.http import HttpRequest, HttpResponse

def questionnaire_response_page(request: HttpRequest, questionnaire_response_id: str) -> HttpResponse:
  return HttpResponse(questionnaire_response_id)