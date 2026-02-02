from django.contrib.auth.models import AbstractUser
from typing import Optional
from provider_intake.models import Provider

class User(AbstractUser):
    provider: Optional["Provider"]

