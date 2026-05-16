from django.core.management.base import BaseCommand 
from django.contrib.auth import get_user_model
from typing import Any
from clinician_overview.models import Client

User = get_user_model()
# get all users
allUsers = User.objects.all()

class Command(BaseCommand):
    help = "Populate the database with sample providers and clients."
    def handle(self, *args: str, **options: Any):
        for user in allUsers:
            Client.objects.create(
                client_id = "sakf2049", 
                clinician = user,
                is_active = True, 
                tags = ["March 2023", "April 2024"]
            )
