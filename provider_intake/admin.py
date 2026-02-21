from django.contrib import admin
from .models import Provider

# Register your models here.
@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin): # type: ignore[type-arg]
    list_display=('first_name', 'last_name', 'scoring_email')