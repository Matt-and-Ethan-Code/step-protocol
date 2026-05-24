from django.http import HttpRequest, JsonResponse
from initial_screening.models import QuestionnaireResponse
from clinician_overview.models import ClientId
import json

def delete_responses_route(request: HttpRequest, client_id:str) -> JsonResponse:
    print("request: ", request.body)
    data = json.loads(request.body)
    delete_responses = data.get('responses')

    if delete_responses is None:
        return JsonResponse({'error': 'Provide responses to delete.'}, status=400)

    # get the relevant user using the client id and clinician
    # should always return a unique client because client identifier string and clinician should form a joint
    # primary key together
    matching_client = ClientId.objects.get(client_id=client_id, clinician=request.user)
    print("matching client: ", matching_client)

    for response in delete_responses:
        response_id = int(response)
        QuestionnaireResponse.objects.filter(id=response_id, user_identifier_id=matching_client.id).delete()

    return JsonResponse({'success': True})