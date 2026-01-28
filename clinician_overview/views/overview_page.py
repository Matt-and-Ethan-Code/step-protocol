from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import django.http as http
# Create your views here.
def overview_page(request: HttpRequest) -> HttpResponse:
  return HttpResponse("hiiiiaaa")