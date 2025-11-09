from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Questionnaire, UserProgress

@login_required
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

@login_required
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
        
        if next_questionnaire:
            progress.current_questionnaire = next_questionnaire.id
            progress.save()
            return redirect('questionnaire_view', questionnaire_id=next_questionnaire.id)
        else:
            progress.completed = True
            progress.save()
            return redirect('testing_complete')
        
    return render(request, 'initial_screening/questionnaire.html', {'questionnaire': questionnaire, 'questionnaire_count': questionnaire_count})

@login_required
def testing_complete(request):
    return render(request, "initial_screening/testing_complete.html")