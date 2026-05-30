from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from clinician_overview.models import  Client, AccessGrant
from django.db.models import Q


def has_access(clinician: User, client: Client, time: datetime | None = None) -> bool:
    time = time or timezone.now()
    access_record_exists = AccessGrant.objects.filter(
        clinician=clinician,
        client_id=client,
        granted_at__lte=time,
    ) \
    .filter(Q(revoked_at__isnull=True) | Q(revoked_at__gt=time)) \
    .filter(Q(expires_at__isnull=True) | Q(expires_at__gt=time)) \
    .exists()
    
    return access_record_exists



def new_grant_until(clinician: User, client: Client, end_date: datetime) -> AccessGrant:
    new_access_grant = AccessGrant(
        client=client,
        clinician=clinician,
        granted_at=timezone.now(),
        expires_at=end_date,
        revoked_at=None,
        notes=None
    )
    return new_access_grant


