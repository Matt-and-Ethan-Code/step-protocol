from django.http import HttpRequest
import initial_screening.scoring as scoring
from django.shortcuts import render
from typing import Any, Callable, Literal

def itq_email(request: HttpRequest):
    context: dict[str, Callable[[bool], Literal["Yes", "No"]] ] = itq_email_template_context("esme!!!", "this is my troubling experience", itq_sample_response())
    return render(request, 'initial_screening/itq_email.html', context)

def itq_sample_response() -> scoring.ItqForm:
    form_response: scoring.ItqForm = {
        1: 1,
        2: 3,

        3: 0,
        4: 1,
        
        5: 2,
        6: 4,
        
        7: 0,
        8: 1,
        9: 4,

        10: 0,
        11: 2,
        
        12: 1,
        13: 2,

        14: 0,
        15: 0,

        16: 1,
        17: 1,
        18: 2,
    }
    return form_response

def itq_email_template_context(client_id: str, troubling_experience: str, form_response: scoring.ItqForm) -> dict[str, Callable[[Any], Literal["Yes", "No"]] ]:
    itq_score = scoring.itq_dichotomous_score(form_response)
    yes_no: Callable[[bool], Literal["Yes", "No"]]  = lambda b: "Yes" if b else "No"
    context: dict[str, Any] = {
        "client_id": client_id,
        "troubling_experience": troubling_experience,
        "responses": form_response,
        "diagnosis": itq_score.diagnosis.upper(),
        "reexperiencing_met": yes_no(itq_score.reexperiencing_met),
        "avoidance_met": yes_no(itq_score.avoidance_met),
        "sense_of_threat_met": yes_no(itq_score.sense_of_threat_met),
        "ptsd_functional_impairment_met": yes_no(itq_score.ptsd_functional_impairment_met),
        "affective_dysregulation_met": yes_no(itq_score.affective_disregulation_met),
        "negative_self_concept_met": yes_no(itq_score.negative_self_concept_met),
        "disturbances_in_relationships_met": yes_no(itq_score.disturbances_in_relationships_met),
        "dso_functional_impairment_met": yes_no(itq_score.dso_functional_impairment_met),
    }
    return context