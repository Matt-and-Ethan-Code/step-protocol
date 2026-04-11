from django.db import models
from .mixins import ReadLoggingManager 

class AuditedModel(models.Model):
    objects = ReadLoggingManager()

    class Meta: 
        abstract = True
