from django.db import models
from clinician_overview.models import Client
# Create your models here.
class SoloResponse(models.Model):
  """
  A STEP Solo response, created when the user is done STEP Solo
  """
  client = models.ForeignKey(Client, on_delete=models.CASCADE)

  stress_before_elements = models.IntegerField()
  stress_after_elements = models.IntegerField()
  step_2 = models.IntegerField()
  step_5pod1_first = models.IntegerField()
  step_5pod1_last = models.IntegerField()
  step_5pod2_first = models.IntegerField()
  step_5pod2_last = models.IntegerField()
  step_5pod3_first = models.IntegerField()
  step_5pod3_last = models.IntegerField()
  step_6 = models.IntegerField()

  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    indexes = [
      models.Index(fields=["client"])
    ]

