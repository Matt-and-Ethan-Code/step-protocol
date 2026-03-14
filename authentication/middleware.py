import time 
from django.conf import settings 
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from typing import Callable

class SessionTimeoutMiddleware: 
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> HttpResponse:
        self.get_response = get_response 

    def __call__(self, request: HttpRequest):
        if request.user.is_authenticated: 
            current_time = time.time()


            # Idle timeout
            last_activity = request.session.get("last_activity")
            if last_activity:
                if current_time - last_activity > settings.SESSION_IDLE_TIMEOUT:
                    logout(request)

            request.session["last_activity"] = current_time

            # absolute timeout 
            login_time = request.session.get("login_time")
            if not login_time:
                request.session["login_time"] = current_time 

            elif current_time - login_time > settings.SESSION_ABSOLUTE_TIMEOUT:
                logout(request)

        return self.get_response(request)