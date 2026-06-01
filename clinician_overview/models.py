from django.db import models
from django.contrib.auth.models import User
from typing import List

class Client(models.Model):
  """
  The record that connects a patient to their clinician.
  """
  client_id = models.CharField(max_length=50)
  clinician = models.ForeignKey(User, on_delete=models.CASCADE)
  is_active: models.BooleanField = models.BooleanField(verbose_name="Is Active", default=True) # type: ignore
  tags: List[str] =models.JSONField(default=list, blank=True) # type: ignore
  
  def __str__(self):
    return self.client_id

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['client_id', 'clinician'],
        name='unique_client_per_clinician'
      )
    ]

class AccessGrant(models.Model):
  """
  Represents a period of access for a user granted by a clinician
  """
  client = models.ForeignKey(Client, on_delete=models.CASCADE)
  clinician = models.ForeignKey(User, on_delete=models.CASCADE)

  created_at = models.DateTimeField(auto_now_add=True)
  granted_at = models.DateTimeField(auto_now_add=True)
  expires_at = models.DateTimeField()
  revoked_at = models.DateTimeField(null=True, blank=True)
  notes = models.TextField(null=True, blank=True)

  class Meta:
    indexes = [
      models.Index(fields=["clinician", "client"]),
      models.Index(fields=["clinician", "client", "granted_at"]),
      models.Index(fields=["clinician", "client", "revoked_at"]),
      models.Index(fields=["clinician", "client", "expires_at"]),
    ]