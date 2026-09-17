from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from step_solo.util.identified import solo_session_required


STRESS_BEFORE_TOKEN = 'solo_stress_before'  # stored as an int
@solo_session_required()
def stress_before_four_elements(request: HttpRequest) -> HttpResponse:
    if request.POST:
        stress_before = request.POST.get(STRESS_BEFORE_TOKEN, default=None)
        if stress_before is None:
            return redirect('solo_stress_before_four_elements') # go back to the get

        try:
            request.session[STRESS_BEFORE_TOKEN] = int(stress_before)
        except ValueError:
            return redirect('solo_stress_before_four_elements')
        return redirect('solo_stress_after_four_elements')
    else:
        existing_stress_before = request.session.get(STRESS_BEFORE_TOKEN)
        stress_levels: list[str] = []
        for stress_level in range(0, 11):
            stress_levels.append(str(stress_level))
        ctx = {
            "title": "Stress Before 4 Elements",
            "preselected_stress_level": str(existing_stress_before),
            "stress_levels": stress_levels,
            "previous_url": "solo_four_elements",
            "next_url": "solo_stress_after_four_elements"
        }
        return render(request, 'step_solo/stress_before_four_elements.html', context=ctx)


