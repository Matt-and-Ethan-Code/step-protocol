from django.shortcuts import render, redirect, get_object_or_404
from initial_screening.models import Questionnaire, QuestionnaireResponse, AnswerOption, ResponseItem
from initial_screening.intake_forms import QuestionnaireForm

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





