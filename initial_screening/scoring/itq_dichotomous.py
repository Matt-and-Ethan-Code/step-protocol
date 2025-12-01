"""
Score the ITQ form according to the dichotomous criteria.
According to https://novopsych.com/assessments/diagnosis/international-trauma-questionnaire-itq/
"""

from dataclasses import dataclass
from typing import Literal
from scoring import ItqResponse, ItqForm, ItqQuestion

@dataclass
class PtsdScore:
    label: Literal['reexperiencing', 'avoidance', 'sense_of_threat', 'ptsd_functional_impairment', 'functional_impairment']
    from_response: ItqQuestion
@dataclass
class DsoScore:
    label: Literal['affective_disregulation', 'negative_self_concept', 'disturbances_in_relationships', 'functional_impairment']
    from_response: ItqQuestion

@dataclass
class ItqDichotomousScore:
    diagnosis: Literal['none', 'ptsd', 'cptsd']
    ptsd_scores: list[PtsdScore]
    dso_scores: list[DsoScore]

def score(responses: ItqForm) -> ItqDichotomousScore:
    """
    Score the full ITQ form according to dichotomous criteria
    """
    ptsd_indicated, ptsd_scores = ptsd_score(responses)
    dso_indicated, dso_scores = dso_score(responses)

    diagnosis: Literal['none', 'ptsd', 'cptsd'] = 'none'
    if ptsd_indicated and dso_indicated:
        diagnosis = 'cptsd'
    elif ptsd_indicated:
        diagnosis = 'ptsd'
    return ItqDichotomousScore(diagnosis=diagnosis, ptsd_scores=ptsd_scores, dso_scores=dso_scores)


def score_significant(score: ItqResponse) -> bool:
    return score >= 2

def ptsd_score(responses: ItqForm) -> tuple[bool, list[PtsdScore]]:
    # PTSD Clusters
    reexperiencing_cluster = ptsd_reexperiencing_score(responses[1], responses[2])
    avoidance_cluster = ptsd_avoidance_score(responses[3], responses[4])
    sense_of_threat_cluster = ptsd_sense_of_threat_score(responses[5], responses[6])

    # PTSD functional impairment
    functional_impairment_cluster = ptsd_functional_impairment_score(responses[7], responses[8], responses[9])

    at_least_one_cluster_met = len(reexperiencing_cluster) > 0 or len(avoidance_cluster) > 0 or len(sense_of_threat_cluster) > 0
    at_least_one_functional_impairment_met = len(functional_impairment_cluster) > 0
    ptsd_indicated = at_least_one_cluster_met and at_least_one_functional_impairment_met

    accumulated_scores: list[PtsdScore] = [*reexperiencing_cluster, *avoidance_cluster, *sense_of_threat_cluster, *functional_impairment_cluster]
    return ptsd_indicated, accumulated_scores

def ptsd_reexperiencing_score(q1: ItqResponse, q2: ItqResponse) -> list[PtsdScore]:
    scores: list[PtsdScore] = []
    if score_significant(q1):
        scores.append(PtsdScore(label='reexperiencing', from_response=1))
    if score_significant(q2):
        scores.append(PtsdScore(label='reexperiencing', from_response=2))
    return scores

def ptsd_avoidance_score(q3: ItqResponse, q4: ItqResponse) -> list[PtsdScore]:
    scores: list[PtsdScore] = []
    if score_significant(q3):
        scores.append(PtsdScore(label='avoidance', from_response=3))
    if score_significant(q4):
        scores.append(PtsdScore(label='avoidance', from_response=4))
    return scores

def ptsd_sense_of_threat_score(q5: ItqResponse, q6: ItqResponse) -> list[PtsdScore]:
    scores: list[PtsdScore] = []
    if score_significant(q5):
        scores.append(PtsdScore(label='sense_of_threat', from_response=5))
    if score_significant(q6):
        scores.append(PtsdScore(label='sense_of_threat', from_response=6))
    return scores


def ptsd_functional_impairment_score(q7: ItqResponse, q8: ItqResponse, q9: ItqResponse) -> list[PtsdScore]:
    scores: list[PtsdScore] = []
    if score_significant(q7):
        scores.append(PtsdScore(label='ptsd_functional_impairment', from_response=7))
    if score_significant(q8):
        scores.append(PtsdScore(label='ptsd_functional_impairment', from_response=8))
    if score_significant(q9):
        scores.append(PtsdScore(label='ptsd_functional_impairment', from_response=9))
    return scores

def dso_affective_disregulation_score(q10: ItqResponse, q11: ItqResponse) -> list[DsoScore]:
    scores: list[DsoScore] = []
    if score_significant(q10):
        scores.append(DsoScore(label='affective_disregulation', from_response=10))
    if score_significant(q11):
        scores.append(DsoScore(label='affective_disregulation', from_response=11))
    return scores

def dso_negative_self_concept_score(q12: ItqResponse, q13: ItqResponse) -> list[DsoScore]:
    scores: list[DsoScore] = []
    if score_significant(q12):
        scores.append(DsoScore(label='negative_self_concept', from_response=12))
    if score_significant(q13):
        scores.append(DsoScore(label='negative_self_concept', from_response=13))
    return scores

def dso_disturbances_in_relationships_score(q14: ItqResponse, q15: ItqResponse) -> list[DsoScore]:
    scores: list[DsoScore] = []
    if score_significant(q14):
        scores.append(DsoScore(label='disturbances_in_relationships', from_response=14))
    if score_significant(q15):
        scores.append(DsoScore(label='disturbances_in_relationships', from_response=15))
    return scores

def dso_functional_impairment_score(q16: ItqResponse, q17: ItqResponse, q18: ItqResponse) -> list[DsoScore]:
    scores: list[DsoScore] = []
    if score_significant(q16):
        scores.append(DsoScore(label='functional_impairment', from_response=17))
    if score_significant(q17):
        scores.append(DsoScore(label='functional_impairment', from_response=17))
    if score_significant(q18):
        scores.append(DsoScore(label='functional_impairment', from_response=18))
    return scores

def dso_score(responses: ItqForm) -> tuple[bool, list[DsoScore]]:
    affective_disregulation_cluster = dso_affective_disregulation_score(responses[10], responses[11])
    negative_self_concept_cluster = dso_negative_self_concept_score(responses[12], responses[13])
    disturbances_in_relationships_cluster = dso_disturbances_in_relationships_score(responses[14], responses[15])


    dso_functional_impairments = dso_functional_impairment_score(responses[16], responses[17], responses[18])
    at_least_one_cluster_met = len(affective_disregulation_cluster) > 0 or len(negative_self_concept_cluster) > 0 or len(disturbances_in_relationships_cluster) > 0
    at_least_one_functional_impairment_met = len(dso_functional_impairments) > 0
    dso_indicated = at_least_one_cluster_met and at_least_one_functional_impairment_met

    accumulated_dso_scores: list[DsoScore] = [*affective_disregulation_cluster, *negative_self_concept_cluster, *disturbances_in_relationships_cluster, *dso_functional_impairments]
    return (dso_indicated, accumulated_dso_scores)
