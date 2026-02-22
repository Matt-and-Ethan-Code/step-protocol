from django.shortcuts import render#, redirect 
from django.http import HttpRequest
def session_expired(request: HttpRequest):
    return render(request, "authentication/session_expired.html")