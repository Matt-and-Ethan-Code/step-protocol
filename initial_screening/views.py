from django.shortcuts import render, redirect, get_object_or_404
from .models import Questionnaire, UserProgress, QuestionnaireResponse
from .intake_forms import QuestionnaireForm
from . import scoring

def home_view(request):
    return render(request, "initial_screening/home_page.html")

def start_testing(request):
    progress, created = UserProgress.objects.get_or_create(user=request.user)
    first_questionnaire = Questionnaire.objects.order_by('order').first()

    if not first_questionnaire:
        progress.completed = True
        progress.save()
        return redirect('testing_complete')

    progress.current_questionnaire = first_questionnaire.id
    progress.completed = False
    progress.save()

    return redirect('questionnaire_view', questionnaire_id=first_questionnaire.id)

def questionnaire_view(request, questionnaire_id):
    progress, created = UserProgress.objects.get_or_create(user=request.user)

    # if questionnaire_id != progress.current_questionnaire:
    #     return redirect('questionnaire_view', questionnaire_id=progress.current_questionnaire)
    
    questionnaire = get_object_or_404(
        Questionnaire.objects.prefetch_related('question_blocks__questions__options'),
        id=questionnaire_id
    )

    questionnaire_count = Questionnaire.objects.count()

    if request.method == 'POST':
        next_questionnaire = (
            Questionnaire.objects 
            .filter(order__gt=questionnaire.order)
            .order_by('order')
            .first()
        )

        answers = request.POST.dict()
        answers.pop('csrfmiddlewaretoken', None)
#        QuestionnaireResponse.objects.create(
 #           questionnaire=questionnaire,
  #          user=request.user
   #     )
        
        request.session[f'questionnaire_{questionnaire.id}_data'] = request.POST

        print("Questoinnaire data: ", request.POST)

        
        if next_questionnaire:
            progress.current_questionnaire = next_questionnaire.id
            progress.save()
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

    itq_score = scoring.itq_dichotomous_score(form_response)

    yes_no = lambda b: "Yes" if b else "No"
    
    context = {
        "client_id": "esme!!!",
        "troubling_experience": "this is my troubling experience",
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
    return render(request, 'initial_screening/itq_email.html', context)