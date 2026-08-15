"""
Use session variables to ensure that users are identified before accessing views.
They are identified with a provided client id + provider.
"""

from django.http import HttpRequest
from django.core.exceptions import PermissionDenied
import clinician_overview.util.client

SOLO_CLIENT_ID_COOKIE = 'solo_client_id'
SOLO_PROVIDER_EMAIL_COOKIE = 'solo_provider_email'
def require_identified(req: HttpRequest, check_db=True) -> tuple[str, str]:
    """
    Returns the (client_id, provider email) tuple.
    """
    client_id: str | None = req.session.get(SOLO_CLIENT_ID_COOKIE)
    if client_id is None:
        raise PermissionDenied(f"{SOLO_CLIENT_ID_COOKIE} not set!")

    provider_email: str | None = req.session.get(SOLO_PROVIDER_EMAIL_COOKIE)
    if provider_email is None:
        raise PermissionDenied(f"{SOLO_PROVIDER_EMAIL_COOKIE} not set!")

    if check_db:
        client = clinician_overview.util.client.find(client_id, provider_email)
        if client is None:
            raise PermissionDenied()
        
    return (client_id, provider_email)


def set_identity(req: HttpRequest, client_id: str, provider_email: str) -> None:
    """
    Set the client id and provider email for the current step solo session.
    """
    req.session[SOLO_CLIENT_ID_COOKIE] = client_id
    req.session[SOLO_PROVIDER_EMAIL_COOKIE] = provider_email
    
    
