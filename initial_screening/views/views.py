from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Questionnaire,  QuestionnaireResponse, ResponseItem, AnswerOption, Question, FormMembership
from ..intake_forms import QuestionnaireForm
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from ..scoring import DesTForm, Dass21Form, GSEForm, ItqForm, Pcl5Form, DesTResponse, DesTQuestion, Dass21Question, Dass21Response, Pcl5Question, Pcl5Response
import initial_screening.scoring as scoring
from typing import Any, cast
from clinician_overview.models import Client
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
    initial_screening_form_id = 1

    return redirect('start_testing', form_id=initial_screening_form_id)
    #return render(request, "initial_screening/home_page.html")

def start_testing(_:HttpRequest, form_id:int):
    # the path to send the user to the first questionnaire in the form
    # questionnaire membership is stored in FormMembership, so we must query it to find the questionnaire in the form
    # with the smallest 'order' value
    first_form_member: FormMembership | None = FormMembership.objects.filter(form_id=form_id).order_by('order').first()
    if first_form_member:
        # check if the form has any members recorded in FormMembership
        first_questionnaire = first_form_member.questionnaire
        # render the questionnaire
        return redirect('questionnaire_view', form_id=form_id, questionnaire_id=first_questionnaire.id)

    # otherwise, the form may not have any members, or the first member didn't have a populated Questionnaire field
    # send the user to the testing_complete page
    return redirect('testing_complete')



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


def questionnaire_view(request: HttpRequest, form_id:int, questionnaire_id: int | None):
    """
    Render a page with a questionnaire.
    form_id: the id of Form (see models).
        
        
    Forms contain multiple questionnaires in a specific order.
    (example: questionnaire A comes first, questionnaire B comes second).
        -   Note: this is stored in FormMembership, not Form.
            This is because Form - Questionnaire is a many-to-many relationship.
    """

    # find the questionnaire based on id
    questionnaire = get_object_or_404(
        Questionnaire.objects.prefetch_related('question_blocks__questions__options'),
        id=questionnaire_id
    )



    questionnaire_count = Questionnaire.objects.count()

    if request.method == 'POST':
        # the user must be submitting answers

        # get the answers as a dictionary
        answers = request.POST.dict()
        # remove csrf token
        # for more information, see: https://docs.djangoproject.com/en/6.0/ref/csrf/ 
        answers.pop('csrfmiddlewaretoken', None)

        # check if this is the initial questionnaire asking the unique ID
        # if yes: it will need to be handled differently 
        #   we will need to store the client ID
        #   that way, when the user submits the next questionnaires in the form (on subsequent pages)
        #   we can use their unique identifier in the submission and tie it back to them

        # get the smallest questionnaire in the form
        # relationships between forms and questionnaires are recorded in FormMembership
        min_relationship = FormMembership.objects.filter(form_id = form_id).order_by('order').first()
        if min_relationship:
            min_questionnaire = min_relationship.questionnaire
            # compare the ID of the smallest questionnaire with the questionnaire ID received in the request path
            # this should be questionnaire 3, "STEP Screening Forms"
            if questionnaire_id == min_questionnaire.id:

                # the question asking the ID will be question 29
                unique_identifier = answers['29']
                # store the unique identifier in a session variable
                request.session['unique_identifier'] = unique_identifier

            # get the user identifier -- at this point it should exist
            user_identifier = request.session.get('unique_identifier')

            client = None

            # check if a client id exists yet
            try:
                # look up the ClientId table on user identifier
                client = Client.objects.get(client_id=user_identifier)
            except Client.DoesNotExist:

                # if objects.get fails, ClientId.DoesNotExist gets thrown
                # must create ClientId

                # get the selected provider -- in question 30
                selected_provider_string = answers['30']
                if isinstance(selected_provider_string, str):
                    # question 30 is a multiple choice question (dropdown), so we must look up its AnswerOption
                    # see models for more information.
                    selected_provider_option = AnswerOption.objects.filter(question_id=30, id=int(selected_provider_string)).first()
                    if (selected_provider_option):
                        # query the users table for a matching provider
                        # the email is stored in the internal_value field
                        clinician = User.objects.get(email=selected_provider_option.internal_value)

                        # create a new client id if not exists
                        # using default values
                        client = Client.objects.create(
                            client_id=user_identifier, 
                            clinician=clinician,
                            is_active=True, 
                            tags=[]
                        )

            # store the QuestionnaireResponse
            # this will not contain any answers, but just the record that the user responded to the questionnaire.
            new_response = QuestionnaireResponse.objects.create(
                questionnaire=questionnaire,
                user_identifier=client, 
                form=min_relationship.form 
                # we previously already received an instance of formmembership, where the form is one of the fields
                # so we can just use that field instead of having to re-query the database
            )

            for answer in answers.keys():
                # go through each answer in the answers dictionary
                # and store each response as a ResponseItem
                question_id = int(answer)
                matching_question = Question.objects.get(id=question_id)
                question_type = matching_question.question_type

                if question_type == "checkbox" or question_type == "radio" or question_type == "dropdown":
                    # examine responses on questions where multiple selections could be possible
                    answer_responses: str | list[str] = answers[answer]
                    # responses will come as a string (if one response) or an array of responses (if multiple responses)
                    # also, these questions may have answer options that contain internal values different from what the user 
                    # saw when selecting the answer (example: they saw the provider name, but selected the questionnaire)
                    # this extra logic is handled by save_answer_response
                    if isinstance(answer_responses, str): 
                        save_answer_response(answer_responses, question_id, new_response)
                    else: 
                        for answer_response in answer_responses:
                            save_answer_response(answer_response, question_id, new_response)
                else:
                    # create a response item just storing the data
                    ResponseItem.objects.create(
                        response = new_response,
                        question_id = question_id,
                        answer = answers[answer]
                    )             


        # query FormMembership for the order of current questionnaire.
        # note: in django, it's possible to filter a database using foreignkey_id=[id] syntax to filter on a foreign key column.
        # example:
        #   FormMembership.objects.filter(questionnaire_id = 4)
        #   when in reality FormMembership doesn't have a questionnaire_id field, only questionnaire
        this_relationship = FormMembership.objects.filter(form_id=form_id).filter(questionnaire_id=questionnaire_id).first()
        if this_relationship:
            # get the next questionnaire in the form
            # there is no db constraint on orders being sequential (example: 6, 7, 8, 9, ...)
            # as a result, gaps are technically possible (example: 6, 9, 10, ...)
            # it's safer to query for the next largest order in form membership
            # as opposed to the order represented by the next sequential integer
            next_questionnaire = FormMembership.objects.filter(form_id=form_id).filter(order__gt=this_relationship.order).order_by('order').first()
        
            # check if the next questionnaire was found
            if next_questionnaire:
                return redirect('questionnaire_view', form_id=next_questionnaire.form.id, questionnaire_id=next_questionnaire.questionnaire.id)
            else:
                # if not found, form must be complete
                # send the user to the testing_complete screen.
                return redirect('testing_complete')

    # for requests other than POST:
    # just render the questionnaire in the request
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
