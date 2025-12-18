from django.shortcuts import render, redirect, get_object_or_404
from .models import Questionnaire, UserProgress, QuestionnaireResponse
from .intake_forms import QuestionnaireForm
from . import scoring

def home_view(request):
    return render(request, "initial_screening/home_page.html")

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
            answer_option_id = None
            try:
                answer_option_id = int(answers[answer])
                matching_option = AnswerOption.objects.filter(question_id=question_id, id=answer_option_id).first()
                if matching_option.internal_value:
                    answer_text = matching_option.internal_value
                else:
                    answer_text = matching_option.text

            except:

                answer_text = answers[answer]


            ResponseItem.objects.create(
                response=new_response,
                question_id=question_id,
                answerID_id=answer_option_id,
                answer=answer_text
            )            
            pass


        next_questionnaire = (
            Questionnaire.objects 
            .filter(order__gt=questionnaire.order)
            .order_by('order')
            .first()
        )



        print("Questionnaire ID: ", questionnaire_id, "Questoinnaire data: ", answers)

        
        if next_questionnaire:
            return redirect('questionnaire_view', questionnaire_id=next_questionnaire.id)
        else:
            progress.completed = True
            progress.save()
            return redirect('testing_complete')
        
    form = QuestionnaireForm(questionnaire, request.POST or None)

    return render(request, 'initial_screening/questionnaire.html', {'form': form, 'questionnaire': questionnaire, 'questionnaire_count': questionnaire_count})

def testing_complete(request):
    return render(request, "initial_screening/testing_complete.html")

def itq_email(request):
    context = itq_email_template_context("esme!!!", "this is my troubling experience", sample_response())
    return render(request, 'initial_screening/itq_email.html', context)

def sample_response() -> scoring.ItqForm:
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

def itq_email_template_context(client_id: str, troubling_experience: str, form_response: scoring.ItqForm):
    itq_score = scoring.itq_dichotomous_score(form_response)
    yes_no = lambda b: "Yes" if b else "No"
    context = {
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



def dass21_sample_response() -> scoring.Dass21Form:
    form_response: scoring.Dass21Form = {
        1: 3,
        2: 3,
        3: 3,
        4: 3,
        5: 3,
        6: 3,
        7: 3,
        8: 3,
        9: 3,
        10: 3,
        11: 3,
        12: 3,
        13: 3,
        14: 3,
        15: 3,
        16: 3,
        17: 3,
        18: 3,
        19: 3,
        20: 3,
        21: 3,
    }
    return form_response

def dass21_email(request):
    context = dass21_email_context("client id", dass21_sample_response())
    return render(request, "initial_screening/dass21_email.html", context)


def dass21_email_context(client_id: str, responses: scoring.Dass21Form):
    score = scoring.dass21_score(responses)

    context = {
      "client_id": client_id,
      "depression_score": score.depression,
      "depression_severity": score.depression_severity,
      "anxiety_score": score.anxiety,
      "anxiety_severity": score.anxiety_severity,
      "stress_score": score.stress,
      "stress_severity": score.stress_severity,
      "total": score.total
    }

    return context