from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from step_solo.util.identified import solo_session_required


STRESS_AFTER_TOKEN='solo_stress_after'
@solo_session_required()
def stress_after_four_elements(request: HttpRequest) -> HttpResponse:
    if request.POST:
        stress_after = request.POST.get(STRESS_AFTER_TOKEN, default=None)
        if stress_after is None:
            return redirect('solo_stress_after_four_elements')
        try:
            request.session[STRESS_AFTER_TOKEN] = int(stress_after)
        except ValueError:
            return redirect('solo_stress_after_four_elements')
        return redirect('solo_1')
    else:
        existing_stress_after = request.session.get(STRESS_AFTER_TOKEN)
        stress_levels: list[str] = []
        for stress_level in range(0, 11):
            stress_levels.append(str(stress_level))
        ctx = {
            "title": "Stress After 4 Elements",
            "preselected_stress_level": str(existing_stress_after),
            "stress_levels": stress_levels,
            "previous_url": "solo_stress_before_four_elements",
            "next_url": "solo_1",
        }
        return render(request, 'step_solo/stress_after_four_elements.html', context=ctx)
    
