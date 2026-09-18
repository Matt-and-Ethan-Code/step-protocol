"""
Use session variables to ensure that users are identified before accessing views.
They are identified with a provided client id + provider.
"""

from django.http import HttpRequest
from django.core.exceptions import PermissionDenied
import clinician_overview.util.client
from functools import wraps
from django.shortcuts import redirect
from step_solo.util.form_tokens import CLIENT_ID_TOKEN, PROVIDER_EMAIL_TOKEN

def require_identified(req: HttpRequest, check_db: bool = True) -> tuple[str, str]:
    """
    Returns the (client_id, provider email) tuple.
    """
    client_id: str | None = req.session.get(CLIENT_ID_TOKEN)
    if client_id is None:
        raise PermissionDenied(f"{CLIENT_ID_TOKEN} not set!")

    provider_email: str | None = req.session.get(PROVIDER_EMAIL_TOKEN)
    if provider_email is None:
        raise PermissionDenied(f"{PROVIDER_EMAIL_TOKEN} not set!")

    if check_db:
        client = clinician_overview.util.client.find(client_id, provider_email)
        if client is None:
            raise PermissionDenied()
        
    return (client_id, provider_email)


def set_identity(req: HttpRequest, client_id: str, provider_email: str) -> None:
    """
    Set the client id and provider email for the current step solo session.
    """
    req.session[CLIENT_ID_TOKEN] = client_id
    req.session[PROVIDER_EMAIL_TOKEN] = provider_email
    
    
def solo_session_required():
    def decorator(view_function):
        @wraps(view_function)
        def _wrapped_view(request: HttpRequest, *args, **kwargs):
            try:
                (_client_id, _provider_email) = require_identified(request, check_db=True)
            except PermissionDenied as e:
                return redirect('solo_index')
            return view_function(request, *args, **kwargs)
        return _wrapped_view
    return decorator
                
