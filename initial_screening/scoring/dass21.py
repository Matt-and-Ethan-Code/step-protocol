"""
DASS-21: Depression, Anxiety, and Stress Scale
"""
from dataclasses import dataclass
from scoring import Dass21Form

@dataclass
class Dass21Score:
    score: int

def score(responses: Dass21Form) -> Dass21Score:
    pass