import logging
from django.db import connection 
from typing import Any, Callable 
from django.http import HttpRequest, HttpResponse 

logger = logging.getLogger(__name__)

class DBReadLoggingMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response 

    def __call__(self, request: HttpRequest) -> HttpResponse: 
        response: Any = self.get_response(request)
        for query in connection.queries:
            if query['sql'].strip().upper().startswith('SELECT'):
                logger.info("DB read", extra={"sql": query['sql'], "time": query['time']})
        return response