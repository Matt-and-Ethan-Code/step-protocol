from django.db import models
from django.db.models import JSONField
from django.conf import settings

class Provider(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        related_name="provider"
    )

    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)

    signup_news=models.BooleanField(default=False)

    scoring_email=models.EmailField()

    phone_country=models.CharField(max_length=6)
    phone_number=models.CharField(max_length=20)

    profession=models.CharField(max_length=50)
    profession_other=models.CharField(max_length=250, blank=True)

    practice_years=models.CharField(max_length=50)

    emdr=models.CharField(max_length=50)
    emdr_other=models.CharField(max_length=250, blank=True)

    practice_setting =JSONField("") # type: ignore[type-arg]
    practice_other=models.TextField(blank=True)

    client_population =JSONField("") # type: ignore[type-arg]
    client_population_other=models.TextField(blank=True)

    access_type=models.CharField(max_length=50)

    country=models.CharField(max_length=200)
    message=models.TextField(blank=True)
