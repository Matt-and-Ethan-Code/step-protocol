from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import boto3

from step_solo.util.identified import require_identified



def what_to_expect(req: HttpRequest) -> HttpResponse:
    (client_id, provider_email) = require_identified(req)
    ctx = {
        "title": "What to Expect"
    }
    
    return render(req, 'step_solo/what_to_expect.html', context=ctx)
