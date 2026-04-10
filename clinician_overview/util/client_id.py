import random

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'
def generate() -> str:
  letters = random.choices(ALPHABET, k=4)
  digits = random.choices(DIGITS, k=3)
  return letters + digits

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