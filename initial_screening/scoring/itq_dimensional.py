from dataclasses import dataclass
from scoring import ItqForm
from typing import Literal, cast

type QualitiativeDescriptor = Literal['minimal', 'mild', 'moderate', 'severe', 'very_severe']
type DimensionalScaleValue = Literal[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]

def validate_dimensional_score(score: DimensionalScaleValue):
    if score < 0 or score > 24:
        raise Exception(f'DimensionalScore is out of range: {score}')
@dataclass
class ItqDimensionalScore:
    ptsd_severity_score: DimensionalScaleValue
    ptsd_qualitative_descriptor: QualitiativeDescriptor
    dso_severity_score: DimensionalScaleValue
    dso_qualitative_descriptor: QualitiativeDescriptor


def score(responses: ItqForm) -> ItqDimensionalScore:
    ptsd_severity = ptsd_score(responses)
    ptsd_descriptor = descriptor_from_score(ptsd_severity)

    dso_severity = dso_score(responses)
    dso_descriptor = descriptor_from_score(dso_severity)
    
    return ItqDimensionalScore(
        ptsd_severity_score=ptsd_severity,
        ptsd_qualitative_descriptor=ptsd_descriptor,
        dso_severity_score=dso_severity,
        dso_qualitative_descriptor=dso_descriptor
    )

def descriptor_from_score(sum_of_scores: DimensionalScaleValue) -> QualitiativeDescriptor:
    validate_dimensional_score(sum_of_scores)
    if sum_of_scores <= 3:
        return 'minimal'  # 0-3
    elif sum_of_scores <= 6:
        return 'mild'  # 4-6
    elif sum_of_scores <= 10:
        return 'moderate'  # 7-10
    elif sum_of_scores <= 16:
        return 'severe'  # 11-16
    else:
        return 'very_severe'  # 17-24

def ptsd_score(responses: ItqForm) -> DimensionalScaleValue:
    # should be in the range 0-24 since each response is in the range of 0-4
    score: int = sum([responses[1], responses[2], responses[3], responses[4], responses[5], responses[6]])
    dimensional_score: DimensionalScaleValue = cast(DimensionalScaleValue, score)
    validate_dimensional_score(dimensional_score)
    return dimensional_score

def dso_score(responses: ItqForm) -> DimensionalScaleValue:
    # should be in the range 0-24 since each response is in the range of 0-4
    score: int = sum([responses[10], responses[11], responses[12], responses[13], responses[14], responses[15]])
    dimensional_score: DimensionalScaleValue = cast(DimensionalScaleValue, score)
    validate_dimensional_score(dimensional_score)
    return dimensional_score