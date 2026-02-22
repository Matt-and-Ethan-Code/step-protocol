import time 
from django.conf import settings 
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from typing import Callable
from django.shortcuts import redirect

class SessionTimeoutMiddleware: 
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response 

    def __call__(self, request: HttpRequest) -> HttpResponse:
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

        elif request.path.startswith("/start/") and "form_started_at" not in request.session:
            request.session["form_started_at"] = time.time()
        elif request.path.startswith("/questionnaire/"): 
            session_start = request.session.get("form_started_at")
            if not session_start or  time.time() - session_start > 60: # 60 seconds
                request.session.flush()
                return redirect("session_expired")
        return self.get_response(request)