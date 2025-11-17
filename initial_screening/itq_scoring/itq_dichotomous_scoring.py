"""
Score the ITQ form according to the dichotomous criteria.
According to https://novopsych.com/assessments/diagnosis/international-trauma-questionnaire-itq/
"""

from dataclasses import dataclass
from typing import Literal
from itq_scoring import ItqResponse, ItqForm, QuestionIndex

@dataclass
class Score:
    label: Literal['reexperiencing', 'avoidance', 'sense_of_threat', 'functional_impairment']
    from_response: QuestionIndex

def dichotomous_score(responses: ItqForm):
    ptsd_significant, ptsd_scores = ptsd_score(responses)

def score_significant(score: ItqResponse) -> bool:
    return score >= 2

def ptsd_score(responses: ItqForm) -> tuple[Literal[True], list[Score]] | tuple[Literal[False], Literal[None]]:
    # PTSD Clusters
    reexperiencing_cluster = ptsd_reexperiencing_score(responses[1], responses[2])
    avoidance_cluster = ptsd_avoidance_score(responses[3], responses[4])
    sense_of_threat_cluster = ptsd_sense_of_threat_score(responses[5], responses[6])

    # PTSD functional impairment
    functional_impairment_cluster = ptsd_functional_impairment_score(responses[7], responses[8], responses[9])

    at_least_one_cluster_met = len(reexperiencing_cluster) > 0 or len(avoidance_cluster) > 0 or len(sense_of_threat_cluster) > 0
    at_least_one_functional_impairment_met = len(functional_impairment_cluster) > 0
    ptsd_indicated = at_least_one_cluster_met and at_least_one_functional_impairment_met


    if ptsd_indicated:
        accumulated_scores: list[Score] = [*reexperiencing_cluster, *avoidance_cluster, *sense_of_threat_cluster, *functional_impairment_cluster]
        return True, accumulated_scores
    else:
        return False, None


def ptsd_reexperiencing_score(q1: ItqResponse, q2: ItqResponse) -> list[Score]:
    scores: list[Score] = []
    if score_significant(q1):
        scores.append(Score(label='reexperiencing', from_response=1))
    if score_significant(q2):
        scores.append(Score(label='reexperiencing', from_response=2))
    return scores

def ptsd_avoidance_score(q3: ItqResponse, q4: ItqResponse) -> list[Score]:
    scores: list[Score] = []
    if score_significant(q3):
        scores.append(Score(label='avoidance', from_response=3))
    if score_significant(q4):
        scores.append(Score(label='avoidance', from_response=4))
    return scores

def ptsd_sense_of_threat_score(q5: ItqResponse, q6: ItqResponse) -> list[Score]:
    scores: list[Score] = []
    if score_significant(q5):
        scores.append(Score(label='sense_of_threat', from_response=5))
    if score_significant(q6):
        scores.append(Score(label='sense_of_threat', from_response=6))
    return scores


def ptsd_functional_impairment_score(q7: ItqResponse, q8: ItqResponse, q9: ItqResponse) -> list[Score]:
    scores: list[Score] = []
    if score_significant(q7):
        scores.append(Score(label='functional_impairment', from_response=7))
    if score_significant(q8):
        scores.append(Score(label='functional_impairment', from_response=8))
    if score_significant(q9):
        scores.append(Score(label='functional_impairment', from_response=9))
    return scores