from dataclasses import dataclass
from typing import Literal
from .dest_types import DesTQuestion, DesTForm

type DesTDescriptor = Literal['low', 'mild', 'moderate', 'high', 'very high']

@dataclass
class DesTScore:
  amnesia_score: int
  amnesia_descriptor: DesTDescriptor
  depersonalisation_score: int
  depersonalisation_descriptor: DesTDescriptor
  absorption_score: int
  absorption_descriptor: DesTDescriptor
  total_score: int

def amnesia_questions() -> list[DesTQuestion]:
  return [3,4,5,8,25,26]
def depersonalisation_questions() -> list[DesTQuestion]:
  return [7,11,12,13,27,28]
def absorption_questions() -> list[DesTQuestion]:
  return [2,14,15,17,18,20]

def descriptor_from_score(score: int) -> DesTDescriptor:
  if score <= 11:
    return 'low'
  elif score <= 19:
    return 'mild'
  elif score <= 29:
    return 'moderate'
  elif score <= 45:
    return 'high'
  else:
    return 'very high'

def score(responses: DesTForm) -> DesTScore:
  def sum_map(questions: list[DesTQuestion]) -> int:
    total = 0
    for question in questions:
      total += responses[question]
    return total
  
  amnesia_score = sum_map(amnesia_questions())
  amnesia_descriptor = descriptor_from_score(amnesia_score)

  depersonalisation_score = sum_map(depersonalisation_questions())
  depersonalisation_descriptor = descriptor_from_score(depersonalisation_score)

  absorption_score = sum_map(absorption_questions())
  absorption_descriptor = descriptor_from_score(absorption_score)
  
  total_score = amnesia_score + depersonalisation_score + absorption_score
  return DesTScore(
    amnesia_score=amnesia_score,
    amnesia_descriptor=amnesia_descriptor,
    depersonalisation_score=depersonalisation_score,
    depersonalisation_descriptor=depersonalisation_descriptor,
    absorption_score=absorption_score,
    absorption_descriptor=absorption_descriptor,
    total_score=total_score
  )

