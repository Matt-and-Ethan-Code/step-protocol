"""
Scoring from https://www.ptsd.va.gov/professional/assessment/documents/using-PCL5.pdf
Found by searching since Olivia did not provide a resource
"""
from scoring import Pcl5Form
from dataclasses import dataclass

@dataclass
class Pcl5Score:
    score: int
    ptsd_indicated: bool


def score_indicates_ptsd(score: int):
    return score > 33

def score(responses: Pcl5Form) -> Pcl5Score:
    score = sum(responses.values())
    ptsd_indicated = score_indicates_ptsd(score) 
    return Pcl5Score(score=score, ptsd_indicated=ptsd_indicated)
