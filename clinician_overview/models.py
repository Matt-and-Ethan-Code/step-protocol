from django.db import models
from django.contrib.auth.models import User

class ClientId(models.Model):
  client_id = models.CharField(max_length=50)
  clinician = models.ForeignKey(User, on_delete=models.CASCADE)
  is_active = models.BooleanField(verbose_name="Is Active", default=True)