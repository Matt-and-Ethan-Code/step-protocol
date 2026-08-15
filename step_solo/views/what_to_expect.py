from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import boto3



def what_to_expect(req: HttpRequest) -> HttpResponse:
    ctx = {
        "title": "What to Expect"
    }
    
    return render(req, 'step_solo/what_to_expect.html', context=ctx)
