from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
import clinician_overview.util.client as clientm
from ..models import Questionnaire,  QuestionnaireResponse, ResponseItem, AnswerOption, Question, FormMembership
from ..intake_forms import QuestionnaireForm
from django.contrib.auth.models import User
from clinician_overview.scoring import DesTForm, Dass21Form, GSEForm, ItqForm, Pcl5Form, DesTResponse, DesTQuestion, Dass21Question, Dass21Response, Pcl5Question, Pcl5Response
import initial_screening.scoring as scoring
from typing import Any, cast
import random
from clinician_overview.util import access as access_module
from django.http import HttpResponseServerError
from dataclasses import dataclass
from clinician_overview.models import Client

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

        client = None

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

            clinician: User | None = None
            # get the selected provider -- in question 30
            selected_provider_string = answers['30']
            if isinstance(selected_provider_string, str):
                # question 30 is a multiple choice question (dropdown), so we must look up its AnswerOption
                # see models for more information.
                selected_provider_option = AnswerOption.objects.filter(question_id=30, id=int(selected_provider_string)).first()
                if (selected_provider_option):
                    # query the users table for a matching provider
                    # the email is stored in the internal_value field
                    clinician = User.objects.filter(email=selected_provider_option.internal_value).first()
            
            if not clinician:
                # if they are in the dropdown list, they should exist as a user in the db
                return HttpResponseServerError()
            

            client: Client | None = clientm.find(str(user_identifier), clinician)

            if not client: # quit early if it doesnt exist
                return render(request, 'initial_screening/client_does_not_exist.html')
            
            # check that the client has access now
            client_can_access = access_module.has_access(clinician, client)
            if not client_can_access:
                return render(request, 'initial_screening/client_does_not_have_access.html')


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

