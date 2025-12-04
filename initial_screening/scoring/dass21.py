"""
DASS-21: Depression, Anxiety, and Stress Scale
"""
from dataclasses import dataclass
from .dass21_types import Dass21Form

@dataclass
class Dass21Score:
    score: int

def score(responses: Dass21Form) -> Dass21Score:
    return Dass21Score(score=0)