from django.http import HttpRequest, JsonResponse
#from initial_screening.models import QuestionnaireResponse
from clinician_overview.models import Client
import json


def delete_clients_route(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    delete_clients = data.get('rows')

    if delete_clients is None:
        return JsonResponse({'error': 'Provide clients to delete.'}, status=400)

    # get the clients using the client ids and clinician
    matching_clients = Client.objects.filter(pk__in=delete_clients, clinician=request.user)
    for client in matching_clients:
        # delete all responses associated with this client
        #QuestionnaireResponse.objects.filter(user_identifier_id=client.pk).delete()
        # delete the client
        client.delete()
        
    return JsonResponse({'success': True})