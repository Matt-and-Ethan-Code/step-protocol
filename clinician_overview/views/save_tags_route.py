import json
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from clinician_overview.models import ClientId
from typing import Any, cast

@require_POST
def save_tags_route(request: HttpRequest, client_id: str):
    print(request.body)
    data: Any = json.loads(request.body)
    tags: list[str] | None = parse_request(data)

    # validate the tags are a list of strings
    if tags is None:
        return JsonResponse({'error': 'tags must be an array of strings'}, status=400)
    
    print("client_id: ", client_id, "user: ", request.user)
    
    client = ClientId.objects.get(client_id=client_id, clinician=request.user)
    print(client)
    client.tags = tags
    client.save()

    return JsonResponse({'success': True})

def parse_request(data: bytes) -> list[str] | None:
    if not isinstance(data, dict): return None

    should_be_obj = cast(dict[str, Any], data)
    tags: list[str] = cast(list[str], should_be_obj.get('tags'))
    
    return tags