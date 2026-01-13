from django.shortcuts import render, redirect, get_object_or_404
from ..models import Questionnaire,  QuestionnaireResponse, ResponseItem, AnswerOption, Question
from ..intake_forms import QuestionnaireForm
from django.db.models import OuterRef, Subquery
from django.db.models.query import QuerySet
from ..scoring import DesTForm, Dass21Form, GSEForm, ItqForm, Pcl5Form
from typing import Literal, TypedDict

class AnswersDict(TypedDict):
    DEST: DesTForm
    DASS: Dass21Form
    GSE: GSEForm
    ITQ: ItqForm
    PCL: Pcl5Form


def home_view(request):
    return redirect('start_testing')
    #return render(request, "initial_screening/home_page.html")

def start_testing(request):
    first_questionnaire = Questionnaire.objects.order_by('order').first()

    if not first_questionnaire:
        return redirect('testing_complete')

    return redirect('questionnaire_view', questionnaire_id=first_questionnaire.id)

def get_answer_text(question_id, form_value):
    try: 
        answer_option_id = int(form_value)
        matching_option = AnswerOption.objects.filter(question_id=question_id, id=answer_option_id).first()
        if matching_option.internal_value:
            return matching_option.internal_value
        else:
            return matching_option.text 
    except:
        return form_value



def questionnaire_view(request, questionnaire_id):
    
    questionnaire = get_object_or_404(
        Questionnaire.objects.prefetch_related('question_blocks__questions__options'),
        id=questionnaire_id
    )

    questionnaire_count = Questionnaire.objects.count()

    if request.method == 'POST':
        answers = request.POST.dict()
        answers.pop('csrfmiddlewaretoken', None)

        # get order of first questionnaire
        min_order = Questionnaire.objects.order_by('order').first().order

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
            matching_question = Question.objects.filter(id=question_id).first()
            question_type = matching_question.question_type

            if question_type == "checkbox" or question_type == "radio" or question_type == "dropdown":
                answer_option_id = int(answers[answer])
                matching_option = AnswerOption.objects.filter(question_id=question_id, id=answer_option_id).first()

                if matching_option.internal_value:
                    ResponseItem.objects.create(
                        response = new_response, 
                        question_id = question_id, 
                        answerID_id = answer_option_id, 
                        answer = matching_option.internal_value
                    )
                else: 
                    ResponseItem.objects.create(
                        response = new_response, 
                        question_id = question_id, 
                        answerID_id = answer_option_id,
                        answer = matching_option.text
                    )
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

def calculate_map(latest_respnoses: QuerySet[QuestionnaireResponse]) -> AnswersDict: 
    answer_maps = {}

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
                answer = answers[i]

                options = list(
                    AnswerOption.objects
                    .filter(question=answer.question)
                    .order_by('order')
                )

                matching_option = [x for x in options if x == answer.answerID]

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

    return answer_maps


def testing_complete(request):
    # retrieve all questionnaire responses
    unique_identifier = request.session.get('unique_identifier')
    latest_response_subquery = (
        QuestionnaireResponse.objects
        .filter(
            user_identifier = unique_identifier,
            questionnaire=OuterRef('questionnaire')
        )
        .order_by('-submitted_at')
        .values('id')[:1]
    )

    latest_responses = (
        QuestionnaireResponse.objects
        .filter(user_identifier=unique_identifier)
        .filter(id=Subquery(latest_response_subquery))
        .select_related('questionnaire')
    )

    answer_maps = calculate_map(latest_responses)

    return render(request, "initial_screening/testing_complete.html")





