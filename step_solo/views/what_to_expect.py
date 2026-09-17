from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.identified import solo_session_required


@solo_session_required()
def what_to_expect(req: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "What to Expect",
        "previous_url": "solo_index",
        "next_url": "solo_self_regulation_strategies",
    }
    
    return render(req, 'step_solo/what_to_expect.html', context=ctx)
