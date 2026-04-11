import random
from clinician_overview.models import ClientId
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'
LENGTH =7

def random_id() -> str:
  letters = random.choices(ALPHABET, k=4)
  digits = random.choices(DIGITS, k=3)
  return ''.join(letters + digits)

def new_id() -> str:
  "Return a new id that isn't in the database yet."
  id = random_id()
  while client_id_exists(id):
    id = random_id()
  return id

def client_id_exists(id: str) -> bool:
  try:
    _existing_id = ClientId.objects.get(client_id=id)
    return True
  except ClientId.DoesNotExist:
    return False

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