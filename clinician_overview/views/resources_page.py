from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def resources_page(req: HttpRequest) -> HttpResponse:
  assert isinstance(req.user, AbstractBaseUser)
  return render(req, 'clinician_overview/resources_page.html', { 'nav_section': 'step-resources' })