import random
from clinician_overview.models import Client
from django.contrib.auth.models import User
from collections.abc import Iterable

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'
LENGTH =7

def random_id() -> str:
  """
  Four letters followed by three numbers.
  """
  letters = random.choices(ALPHABET, k=4)
  digits = random.choices(DIGITS, k=3)
  return ''.join(letters + digits)

def new_id() -> str:
  "Return a new id that isn't in the database yet."
  id = random_id()

  while exists(id):
    id = random_id()
  return id

def exists(id: str) -> bool:
  return Client.objects.filter(client_id=id).exists()

def find(client_id: str, clinician: User | str) -> Client | None:
  """
  Lookup a client based on their id and clinician.
  clinician may be the clinician user, or the clinician's email (the lookup back to the user table will be done)
  """
  clinician_user = _clinician_from_email_or_user(clinician)
  # if the clinician doesn't exist, can't look up the client so quit
  if clinician_user is None:
    return None

  # now find the client associated to the clinician
  try:
    existing_client = Client.objects.get(client_id=client_id, clinician=clinician_user)
    return existing_client
  except Client.DoesNotExist:
    return None

def is_valid(maybe_client_id: str) -> bool:
  if len(maybe_client_id) != 7:
    return False
  
  should_be_letters = maybe_client_id[:4]
  for letter in should_be_letters:
    if not letter in ALPHABET:
      return False
  
  should_be_digits = maybe_client_id[4:]
  for digit in should_be_digits:
    if not digit in DIGITS:
      return False
  
  return True

def clients_for_clinician(clinician: User | str) -> Iterable[Client]:
  clinician_user = _clinician_from_email_or_user(clinician)
  if clinician_user is None:
    return []
  return Client.objects.filter(clinician=clinician_user)

def _clinician_from_email_or_user(clinician: User | str) -> User | None:
  clinician_user: User | None = None
  if isinstance(clinician, str):
    # the clinician email was provided, so we need to lookup the user
    try:
      clinician_user = User.objects.get(email=clinician)
    except User.DoesNotExist:
      clinician_user = None
  else:
    clinician_user = clinician
  return clinician_user
