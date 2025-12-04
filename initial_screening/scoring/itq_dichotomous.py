"""
Score the ITQ form according to the dichotomous criteria.
According to https://novopsych.com/assessments/diagnosis/international-trauma-questionnaire-itq/
"""

from dataclasses import dataclass
from typing import Literal
from .itq_types import ItqResponse, ItqForm, ItqQuestion

@dataclass
class PtsdScoreReason:
    label: Literal['reexperiencing', 'avoidance', 'sense_of_threat', 'ptsd_functional_impairment', 'functional_impairment']
    from_response: ItqQuestion
@dataclass
class DsoScoreReason:
    label: Literal['affective_disregulation', 'negative_self_concept', 'disturbances_in_relationships', 'functional_impairment']
    from_response: ItqQuestion

@dataclass
class ItqDichotomousScore:
    diagnosis: Literal['none', 'ptsd', 'cptsd']
    ptsd_reasons: list[PtsdScoreReason]
    reexperiencing_met: bool
    avoidance_met: bool
    sense_of_threat_met: bool
    ptsd_functional_impairment_met: bool
    dso_reasons: list[DsoScoreReason]
    affective_disregulation_met: bool
    negative_self_concept_met: bool
    disturbances_in_relationships_met: bool
    dso_functional_impairment_met: bool

def score(responses: ItqForm) -> ItqDichotomousScore:
    """
    Score the full ITQ form according to dichotomous criteria
    """
    ptsd: PtsdScore = ptsd_score(responses)
    dso = dso_score(responses)

    diagnosis: Literal['none', 'ptsd', 'cptsd'] = 'none'
    if ptsd.indicated and dso.indicated:
        diagnosis = 'cptsd'
    elif ptsd.indicated:
        diagnosis = 'ptsd'
    return ItqDichotomousScore(
        diagnosis=diagnosis,
        ptsd_reasons=ptsd.reasons,
        reexperiencing_met=ptsd.reexperiencing_met,
        avoidance_met=ptsd.avoidance_met,
        sense_of_threat_met=ptsd.sense_of_threat_met,
        ptsd_functional_impairment_met=ptsd.functional_impairment_met,
        dso_reasons=dso.reasons,
        affective_disregulation_met=dso.affective_disregulation_met,
        negative_self_concept_met=dso.negative_self_concept_met,
        disturbances_in_relationships_met=dso.disturbances_in_relationships_met,
        dso_functional_impairment_met=dso.functional_impairment_met
    )


def score_significant(score: ItqResponse) -> bool:
    return score >= 2

@dataclass
class PtsdScore:
    indicated: bool
    reasons: list[PtsdScoreReason]
    reexperiencing_met: bool
    avoidance_met: bool
    sense_of_threat_met: bool
    functional_impairment_met: bool

def ptsd_score(responses: ItqForm) -> PtsdScore:
    # PTSD Clusters
    reexperiencing_cluster = ptsd_reexperiencing_score(responses[1], responses[2])
    avoidance_cluster = ptsd_avoidance_score(responses[3], responses[4])
    sense_of_threat_cluster = ptsd_sense_of_threat_score(responses[5], responses[6])

    # PTSD functional impairment
    functional_impairment_cluster = ptsd_functional_impairment_score(responses[7], responses[8], responses[9])
    reexperiencing_met = len(reexperiencing_cluster) > 0
    avoidance_met = len(avoidance_cluster) > 0
    sense_of_threat_met = len(sense_of_threat_cluster) > 0
    functional_impairment_met = len(functional_impairment_cluster) > 0

    at_least_one_cluster_met = len(reexperiencing_cluster) > 0 or len(avoidance_cluster) > 0 or len(sense_of_threat_cluster) > 0
    at_least_one_functional_impairment_met = len(functional_impairment_cluster) > 0
    ptsd_indicated = at_least_one_cluster_met and at_least_one_functional_impairment_met

    accumulated_scores: list[PtsdScoreReason] = [*reexperiencing_cluster, *avoidance_cluster, *sense_of_threat_cluster, *functional_impairment_cluster]
    return PtsdScore(
        indicated=ptsd_indicated,
        reasons=accumulated_scores,
        reexperiencing_met=reexperiencing_met,
        avoidance_met=avoidance_met,
        sense_of_threat_met=sense_of_threat_met,
        functional_impairment_met=functional_impairment_met
    )

def ptsd_reexperiencing_score(q1: ItqResponse, q2: ItqResponse) -> list[PtsdScoreReason]:
    scores: list[PtsdScoreReason] = []
    if score_significant(q1):
        scores.append(PtsdScoreReason(label='reexperiencing', from_response=1))
    if score_significant(q2):
        scores.append(PtsdScoreReason(label='reexperiencing', from_response=2))
    return scores

def ptsd_avoidance_score(q3: ItqResponse, q4: ItqResponse) -> list[PtsdScoreReason]:
    scores: list[PtsdScoreReason] = []
    if score_significant(q3):
        scores.append(PtsdScoreReason(label='avoidance', from_response=3))
    if score_significant(q4):
        scores.append(PtsdScoreReason(label='avoidance', from_response=4))
    return scores

def ptsd_sense_of_threat_score(q5: ItqResponse, q6: ItqResponse) -> list[PtsdScoreReason]:
    scores: list[PtsdScoreReason] = []
    if score_significant(q5):
        scores.append(PtsdScoreReason(label='sense_of_threat', from_response=5))
    if score_significant(q6):
        scores.append(PtsdScoreReason(label='sense_of_threat', from_response=6))
    return scores


def ptsd_functional_impairment_score(q7: ItqResponse, q8: ItqResponse, q9: ItqResponse) -> list[PtsdScoreReason]:
    scores: list[PtsdScoreReason] = []
    if score_significant(q7):
        scores.append(PtsdScoreReason(label='ptsd_functional_impairment', from_response=7))
    if score_significant(q8):
        scores.append(PtsdScoreReason(label='ptsd_functional_impairment', from_response=8))
    if score_significant(q9):
        scores.append(PtsdScoreReason(label='ptsd_functional_impairment', from_response=9))
    return scores

def dso_affective_disregulation_score(q10: ItqResponse, q11: ItqResponse) -> list[DsoScoreReason]:
    scores: list[DsoScoreReason] = []
    if score_significant(q10):
        scores.append(DsoScoreReason(label='affective_disregulation', from_response=10))
    if score_significant(q11):
        scores.append(DsoScoreReason(label='affective_disregulation', from_response=11))
    return scores

def dso_negative_self_concept_score(q12: ItqResponse, q13: ItqResponse) -> list[DsoScoreReason]:
    scores: list[DsoScoreReason] = []
    if score_significant(q12):
        scores.append(DsoScoreReason(label='negative_self_concept', from_response=12))
    if score_significant(q13):
        scores.append(DsoScoreReason(label='negative_self_concept', from_response=13))
    return scores

def dso_disturbances_in_relationships_score(q14: ItqResponse, q15: ItqResponse) -> list[DsoScoreReason]:
    scores: list[DsoScoreReason] = []
    if score_significant(q14):
        scores.append(DsoScoreReason(label='disturbances_in_relationships', from_response=14))
    if score_significant(q15):
        scores.append(DsoScoreReason(label='disturbances_in_relationships', from_response=15))
    return scores

def dso_functional_impairment_score(q16: ItqResponse, q17: ItqResponse, q18: ItqResponse) -> list[DsoScoreReason]:
    scores: list[DsoScoreReason] = []
    if score_significant(q16):
        scores.append(DsoScoreReason(label='functional_impairment', from_response=17))
    if score_significant(q17):
        scores.append(DsoScoreReason(label='functional_impairment', from_response=17))
    if score_significant(q18):
        scores.append(DsoScoreReason(label='functional_impairment', from_response=18))
    return scores

@dataclass
class DsoScore:
    indicated: bool
    reasons: list[DsoScoreReason]
    affective_disregulation_met: bool
    negative_self_concept_met: bool
    disturbances_in_relationships_met: bool
    functional_impairment_met: bool
def dso_score(responses: ItqForm) -> DsoScore:
    affective_disregulation_cluster = dso_affective_disregulation_score(responses[10], responses[11])
    negative_self_concept_cluster = dso_negative_self_concept_score(responses[12], responses[13])
    disturbances_in_relationships_cluster = dso_disturbances_in_relationships_score(responses[14], responses[15])


    dso_functional_impairments = dso_functional_impairment_score(responses[16], responses[17], responses[18])
    affective_disregulation_met = len(affective_disregulation_cluster) > 0
    negative_self_concept_met = len(negative_self_concept_cluster) > 0
    disturbances_in_relationships_met = len(disturbances_in_relationships_cluster) > 0
    functional_impairment_met = len(dso_functional_impairments) > 0

    at_least_one_cluster_met = affective_disregulation_met or negative_self_concept_met or disturbances_in_relationships_met
    at_least_one_functional_impairment_met = functional_impairment_met
    dso_indicated = at_least_one_cluster_met and at_least_one_functional_impairment_met

    accumulated_dso_scores: list[DsoScoreReason] = [*affective_disregulation_cluster, *negative_self_concept_cluster, *disturbances_in_relationships_cluster, *dso_functional_impairments]
    return DsoScore(
        indicated=dso_indicated,
        reasons=accumulated_dso_scores,
        affective_disregulation_met=affective_disregulation_met,
        negative_self_concept_met=negative_self_concept_met,
        disturbances_in_relationships_met=disturbances_in_relationships_met,
        functional_impairment_met=functional_impairment_met
    )
