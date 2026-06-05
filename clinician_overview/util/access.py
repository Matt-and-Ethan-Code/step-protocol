import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from clinician_overview.models import  Client, AccessGrant
from django.db.models import Q
from django.db.models.manager import BaseManager


def has_access(clinician: User, client: Client, time: datetime.datetime | None = None) -> AccessGrant | None:
    """
    Return an AccessGrant that is currently active as proof that the client currently has access to STEP.
    """
    return _active_access_grants(clinician, client, time).first()




def new_grant_until(clinician: User, client: Client, end_date: datetime.datetime) -> AccessGrant:
    """
    Create a new AccessGrant from now until the provided end date.
    This does not save the AccessGrant to the database, so you need to call access_grant.save() to do that.
    """
    new_access_grant = AccessGrant(
        client=client,
        clinician=clinician,
        granted_at=timezone.now(),
        expires_at=end_date,
        revoked_at=None,
        notes=None
    )
    return new_access_grant

def has_access_until(client: Client) -> datetime.datetime | None:
    latest_date_in_active_access_grants: datetime.datetime | None = _active_access_grants(client.clinician, client) \
        .order_by("-expires_at") \
        .values_list("expires_at", flat=True) \
        .first()

    return latest_date_in_active_access_grants

def _active_access_grants(clinician: User, client: Client, time: datetime.datetime | None = None) -> BaseManager[AccessGrant]:
    time = time or timezone.now()
    access_records = AccessGrant.objects.filter(
        clinician=clinician,
        client=client,
        granted_at__lte=time,
    ) \
    .filter(Q(revoked_at__isnull=True) | Q(revoked_at__gt=time)) \
    .filter(Q(expires_at__isnull=True) | Q(expires_at__gt=time))
    return access_records

def revoke_current_access_for(clinician: User, client: Client) -> None:
    """
    Revoke access for a client right now.
    """
    active_grants = _active_access_grants(clinician, client)
    now = timezone.now()
    _updated_count = active_grants.update(revoked_at=now)


def extend_access(clinician: User, client: Client, num_days: int) -> AccessGrant:
    """
    Extend access for a client by a certain number of days.
    """
    assert num_days > 0
    
    now = timezone.now()
    latest_date_in_active_access_grants: datetime.datetime | None = has_access_until(client)

    duration = datetime.timedelta(days=num_days)
    if latest_date_in_active_access_grants:
        end_date = latest_date_in_active_access_grants + duration
    else:
        end_date = now + duration
    new_grant = new_grant_until(clinician, client, end_date)
    new_grant.save()
    return new_grant
        
    

    
    
