"""
Use this: https://onlinelibrary.wiley.com/doi/pdf/10.1002/9781118093146.app1
"""

from dataclasses import dataclass
from .dest_types import DesTForm

@dataclass
class DesTScore:
  score: int
  significant: bool

def score(responses: DesTForm) -> DesTScore: 
  """
  Returns the score, which is the mean of the responses.
  Significant if the mean is >= 20%.
  """
  question_count = 8
  score = sum(responses.keys()) // question_count # the average among the 8 questions

  return DesTScore(
    score=score,
    significant=score >= 20
  )

