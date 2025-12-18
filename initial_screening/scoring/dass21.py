"""
DASS-21: Depression, Anxiety, and Stress Scale
From https://novopsych.com/assessments/depression/depression-anxiety-stress-scales-short-form-dass-21/
"""
from dataclasses import dataclass
from .dass21_types import Dass21Form, Dass21Severity, Dass21Question

@dataclass
class Dass21Score:
    depression: int
    depression_severity: Dass21Severity
    anxiety: int
    anxiety_severity: Dass21Severity
    stress: int
    stress_severity: Dass21Severity
    total: int

def score(responses: Dass21Form) -> Dass21Score:
    def sum_question_responses(questions: list[Dass21Question]) -> int:
        total = 0
        for question in questions:
            total += responses[question]
        return total
    
    depression_score: int = sum_question_responses(questions_depression())
    depression_severity = severity_label_depression(depression_score)

    anxiety_score = sum_question_responses(questions_anxiety())
    anxiety_severity = severity_label_anxiety(anxiety_score)

    stress_score = sum_question_responses(questions_stress())
    stress_severity = severity_label_stress(stress_score)
    
    total_score = sum([depression_score, anxiety_score, stress_score])

    return Dass21Score(
        depression=depression_score,
        depression_severity=depression_severity,
        anxiety=anxiety_score,
        anxiety_severity=anxiety_severity,
        stress=stress_score,
        stress_severity=stress_severity,
        total=total_score
    )

def questions_depression() -> list[Dass21Question]:
    return [3,5,10,13,16,17,21]

def questions_anxiety() -> list[Dass21Question]:
    return [2,4,7,9,15,19,20]

def questions_stress() -> list[Dass21Question]:
    return [1,6,8,11,12,14,18]

def severity_label_depression(depression_score: int) -> Dass21Severity:
    assert depression_score >= 0
    if depression_score <= 9:
        return 'normal'
    elif depression_score <= 13:
        return 'moderate'
    elif depression_score <= 20:
        return 'severe'
    else:
        return 'extremely severe'
def severity_label_anxiety(anxiety_score: int) -> Dass21Severity:
    assert anxiety_score >= 0
    if anxiety_score <= 7:
        return 'normal'
    elif anxiety_score <= 9:
        return 'mild'
    elif anxiety_score <= 14:
        return 'moderate'
    elif anxiety_score <= 19:
        return 'severe'
    else:
        return 'extremely severe'
def severity_label_stress(stress_score: int) -> Dass21Severity:
    assert stress_score >= 0
    if stress_score <= 14:
        return 'normal'
    elif stress_score <= 18:
        return 'mild'
    elif stress_score <= 25:
        return 'moderate'
    elif stress_score <= 33:
        return 'severe'
    else:
        return 'extremely severe'