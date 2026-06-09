from django.db.models.manager import BaseManager
from clinician_overview.scoring.dass21 import Dass21Score
from clinician_overview.scoring.dass21_types import Dass21Form, Dass21Question, Dass21Response
from clinician_overview.scoring.dest import DesTScore
from clinician_overview.scoring.dest_types import DesTForm, DesTQuestion, DesTResponse
from clinician_overview.scoring.gse import GSEScore
from clinician_overview.scoring.gse_types import GSEForm, GSEQuestion, GSEResponse
from clinician_overview.scoring.gse_types import GSEForm
from clinician_overview.scoring.itq_dichotomous import ItqDichotomousScore
from clinician_overview.scoring.itq_types import ItqForm, ItqResponse, ItqQuestion
from clinician_overview.scoring.pcl5_diagnostic import Pcl5Score
from clinician_overview.scoring.pcl5_types import Pcl5Form, Pcl5Question, Pcl5Response
from initial_screening.models import ResponseItem, AnswerOption
from typing import Callable,  cast
import clinician_overview.scoring as scoring

def build_response_form[TResponse, TQuestion](
    response_items: BaseManager[ResponseItem],
    question_indices: range,
    response_mapper: Callable[[int], TResponse],
    question_cast: Callable[[int], TQuestion],
) -> dict[TQuestion, TResponse]:
    response_form: dict[TQuestion, TResponse] = {}
    for i, item in enumerate(response_items):
        #if item.answerID is None or i not in question_indices:
        #   continue

        count = AnswerOption.objects.filter(
            question=item.question,
            order__lt=item.answerID.order if item.answerID is not None else 0
        ).count()
        response_form[question_cast(i)] = response_mapper(count)

    return response_form

def score_questionnaire_response(responseItems: BaseManager[ResponseItem], questionnaire_title: str) -> ItqDichotomousScore | DesTScore | Pcl5Score | Dass21Score | GSEScore | None:
    if "DES-T" in questionnaire_title:
        destResponseForm: DesTForm = build_response_form(
        responseItems,
        range(1, 29),
        lambda count: cast(DesTResponse, count * 10),
        lambda i: cast(DesTQuestion, i + 1),
        )

        return scoring.dest_score(destResponseForm)
    elif "ITQ" in questionnaire_title: 
        itqResponseForm: ItqForm = build_response_form(
        responseItems,
        range(1, 19),
        lambda count: cast(ItqResponse, count),
        lambda i: cast(ItqQuestion, i),
        )
        traumatic_experience = responseItems.filter(question_id=9).first()
        if traumatic_experience:
            return scoring.itq_dichotomous_score(itqResponseForm, traumatic_experience.answer)
        else:
            return scoring.itq_dichotomous_score(itqResponseForm, "")
    elif "PCL-5" in questionnaire_title:
        pclResponseForm: Pcl5Form = build_response_form(
        responseItems,
        range(1, 21),
        lambda count: cast(Pcl5Response, count),
        lambda i: cast(Pcl5Question, i + 1),
        )
        score = scoring.pcl5_score(pclResponseForm)
        return score
    elif "DASS-21" in questionnaire_title:
        dassResponseForm: Dass21Form = build_response_form(
        responseItems,
        range(1, 22),
        lambda count: cast(Dass21Response, count),
        lambda i: cast(Dass21Question, i + 1),
        )
        dass_score: Dass21Score = scoring.dass21_score(dassResponseForm)
        return dass_score
    elif "GSE" in questionnaire_title:
        gseResponseForm: GSEForm = build_response_form(
        responseItems,
        range(1, 22),
        lambda count: cast(GSEResponse, count),
        lambda i: cast(GSEQuestion, i),
        )
        gse_score: GSEScore = scoring.gse_score(gseResponseForm)
        return gse_score
