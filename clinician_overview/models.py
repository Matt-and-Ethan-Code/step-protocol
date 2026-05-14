from django.db import models
from django.contrib.auth.models import User
from typing import List

class ClientId(models.Model):
  client_id = models.CharField(max_length=50)
  clinician = models.ForeignKey(User, on_delete=models.CASCADE)
  is_active: models.BooleanField = models.BooleanField(verbose_name="Is Active", default=True) # type: ignore
  tags: List[str] =models.JSONField(default=list, blank=True) # type: ignore

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['client_id', 'clinician'],
        name='unique_client_per_clinician'
      )
    ]