from dataclasses import dataclass
from .gse_types import GSEForm


@dataclass
class GSEScore:
  score: int

def score(responses: GSEForm) -> GSEScore:
  total = 0
  for response in responses.values():
    total += response
  return GSEScore(score=total)
