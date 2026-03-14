from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Questionnaire,  QuestionnaireResponse, ResponseItem, AnswerOption, Question
from ..intake_forms import QuestionnaireForm
from django.db.models.query import QuerySet
from ..scoring import DesTForm, Dass21Form, GSEForm, ItqForm, Pcl5Form, DesTResponse, DesTQuestion, Dass21Question, Dass21Response, Pcl5Question, Pcl5Response
import initial_screening.scoring as scoring
from typing import Any, cast
import random
from dataclasses import dataclass
@dataclass
class AnswersDict:
    DEST: DesTForm
    DASS: Dass21Form
    GSE: GSEForm
    ITQ: ItqForm
    PCL: Pcl5Form


def home_view(_: HttpRequest):
    return redirect('start_testing')
    #return render(request, "initial_screening/home_page.html")

def start_testing(_: HttpRequest):
    first_questionnaire: Questionnaire | None = Questionnaire.objects.order_by('order').first()

    if not first_questionnaire:
        return redirect('testing_complete')

    return redirect('questionnaire_view', questionnaire_id=first_questionnaire.id)

def get_answer_text(question_id: int, form_value: str):
    try: 
        answer_option_id = int(form_value)
        matching_option: AnswerOption | None = AnswerOption.objects.filter(question_id=question_id, id=answer_option_id).first()
        if matching_option and matching_option.internal_value:
            return matching_option.internal_value
        elif matching_option:
            return matching_option.text 
    except:
        return form_value

def save_answer_response(option_id: str, question_id: int, new_response: QuestionnaireResponse):
    answer_option_id = int(option_id)
    matching_option = AnswerOption.objects.filter(question_id=question_id, id=answer_option_id).first()

    if matching_option and matching_option.internal_value:
        ResponseItem.objects.create(
            response = new_response, 
            question_id = question_id, 
            answerID_id = answer_option_id, 
            answer = matching_option.internal_value
        )
    elif matching_option: 
        ResponseItem.objects.create(
            response = new_response, 
            question_id = question_id, 
            answerID_id = answer_option_id,
            answer = matching_option.text
        )


def questionnaire_view(request: HttpRequest, questionnaire_id: int | None):
    
    questionnaire = get_object_or_404(
        Questionnaire.objects.prefetch_related('question_blocks__questions__options'),
        id=questionnaire_id
    )

    questionnaire_count = Questionnaire.objects.count()

    if request.method == 'POST':
        answers = request.POST.dict()
        answers.pop('csrfmiddlewaretoken', None)

        # get order of first questionnaire
        min_questionnaire: Questionnaire | None = Questionnaire.objects.order_by('order').first()
        if min_questionnaire:
            min_order = min_questionnaire.order

            # check if first questionnaire
            if questionnaire.order == min_order:
                unique_identifier = answers['29']
                request.session['unique_identifier'] = unique_identifier
            user_identifier = request.session.get('unique_identifier')

            new_response = QuestionnaireResponse.objects.create(
                questionnaire=questionnaire,
                user_identifier=user_identifier
            )

            for answer in answers.keys():
                question_id = int(answer)
                matching_question = Question.objects.get(id=question_id)
                question_type = matching_question.question_type

                if question_type == "checkbox" or question_type == "radio" or question_type == "dropdown":
                    answer_responses: str | list[str] = answers[answer]
                    if isinstance(answer_responses, str): 
                        save_answer_response(answer_responses, question_id, new_response)
                    else: 
                        for answer_response in answer_responses:
                            save_answer_response(answer_response, question_id, new_response)
                else:
                    ResponseItem.objects.create(
                        response = new_response,
                        question_id = question_id,
                        answer = answers[answer]
                    )             


        next_questionnaire = (
            Questionnaire.objects 
            .filter(order__gt=questionnaire.order)
            .order_by('order')
            .first()
        )

        
        if next_questionnaire:
            return redirect('questionnaire_view', questionnaire_id=next_questionnaire.id)
        else:
            return redirect('testing_complete')
        
    form = QuestionnaireForm(questionnaire, request.POST or None)

    return render(request, 'initial_screening/questionnaire.html', {'form': form, 'questionnaire': questionnaire, 'questionnaire_count': questionnaire_count})

def calculate_map(latest_responses: QuerySet[QuestionnaireResponse]) -> AnswersDict: 
    answer_maps: dict[str, Any] = {}

    for q_response in latest_responses:
        answers = (ResponseItem.objects
        .filter(response=q_response)
        .select_related('question')
        .order_by('question__order')
        )

        
        if ("DES-T" not in q_response.questionnaire.name) and ("DASS-21" not in q_response.questionnaire.name) and ("GSE" not in q_response.questionnaire.name) and ("ITQ" not in q_response.questionnaire.name) and ("PCL-5" not in q_response.questionnaire.name):
            print("Encountered unhandled answer", q_response.questionnaire.name)
        else:
            answers = (
                ResponseItem.objects
                .filter(response=q_response)
                .select_related('question', 'answerID')
                .order_by('question__order')
            )

            dest_map = {}

            for i in range(len(answers)):
                question_index = i + 1
                answer: ResponseItem = answers[i]

                options = list(
                    AnswerOption.objects
                    .filter(question=answer.question)
                    .order_by('order')
                )

                relevant_question_option: AnswerOption | None = answer.answerID
                if relevant_question_option:
                    matching_option = [x for x in options if x == answer.answerID]
                else: 

                    matching_option = []

                if len(matching_option) == 0:
                    # text-only answer, no answer options
                    continue
                matching_option = matching_option[0]
                matching_option_index = options.index(matching_option)

                # one-indexed
                if ("GSE" in q_response.questionnaire.name):
                    matching_option_index += 1
                elif ("DES-T" in q_response.questionnaire.name):
                    matching_option_index *= 10

                dest_map[question_index] = matching_option_index

            answer_maps[q_response.questionnaire.name] = dest_map

    dest_key = next((k for k in answer_maps if "DES-T" in k), None)
    dass_key = next((k for k in answer_maps if "DASS" in k), None)
    pcl_key = next((k for k in answer_maps if "PCL" in k), None)
    itq_key = next((k for k in answer_maps if "ITQ" in k), None)
    gse_key = next((k for k in answer_maps if "GSE" in k), None)

    if dest_key and dass_key and pcl_key and itq_key and gse_key:
        answersDict = AnswersDict(
            DEST=answer_maps[dest_key], 
            DASS=answer_maps[dass_key],
            GSE=answer_maps[gse_key],
            ITQ=answer_maps[itq_key],
            PCL=answer_maps[pcl_key]
        )
        return answersDict
    else:
        raise Exception("Could not find responses for one of: DES-T, DASS, PCL, ITQ, GSE.")


def testing_complete(request: HttpRequest):
    # retrieve all questionnaire responses
    # unique_identifier = request.session.get('unique_identifier')
    # latest_response_subquery = (
    #     QuestionnaireResponse.objects
    #     .filter(
    #         user_identifier = unique_identifier,
    #         questionnaire=OuterRef('questionnaire')
    #     )
    #     .order_by('-submitted_at')
    #     .values('id')[:1]
    # )

    # latest_responses = (
    #     QuestionnaireResponse.objects
    #     .filter(user_identifier=unique_identifier)
    #     .filter(id=Subquery(latest_response_subquery))
    #     .select_related('questionnaire')
    # )

    #answer_maps = calculate_map(latest_responses)

    return render(request, "initial_screening/testing_complete.html")





def summary_email_context(client_id: str, itq_troubling_experience: str, responses_map: AnswersDict) -> dict[str, Any]:
    # these have less information and no pre-existing email template
    gse_score = scoring.gse_score(responses_map.GSE)
    dest_score = scoring.dest_score(responses_map.DEST)
    from .itq_sample import itq_email_template_context
    from .dass21_sample import dass21_email_context
    from .pcl5_sample import pcl5_email_context
    return {
        "client_id": client_id,
        "itq_troubling_experience": itq_troubling_experience,
        "ITQ": itq_email_template_context(client_id, itq_troubling_experience, responses_map.ITQ),
        "DASS": dass21_email_context(client_id, responses_map.DASS),
        "GSE": gse_score,
        "PCL": pcl5_email_context(client_id, responses_map.PCL),
        "DEST": dest_score
    }

def summary_email_preview(request: HttpRequest):
    itq_form: scoring.ItqForm = {
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

    gse_form: scoring.GSEForm = {
        1:2,
        2:2,
        3:2,
        4:2,
        5:2,
        6:2,
        7:2,
        8:2,
        9:2,
        10:2,
    }

    
    dest_form: scoring.DesTForm = {
        cast(DesTQuestion, key): cast(DesTResponse, random.randint(0,10)*10) 
        for key in range(1,28+1)
        }
    dass_form: scoring.Dass21Form = {
        cast(Dass21Question, key): cast(Dass21Response, random.randint(0,3) )
        for key in range(1, 21+1) 
        }
    pcl_form: scoring.Pcl5Form = { 
                                    cast(Pcl5Question, key): cast(Pcl5Response, random.randint(0,4)) 
                                    for key in range(1, 20+1)
                                }

    answers_dict = AnswersDict(ITQ=itq_form, GSE=gse_form, DEST=dest_form, DASS=dass_form, PCL=pcl_form)
    ctx = summary_email_context("this is a client id", "this is a significant event", answers_dict)

    return render(request, "initial_screening/summary_email.html", ctx)