import initial_screening.scoring as scoring
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string


def dass21_email(request):

    if False:
        # send itq email
        itq_email = EmailMultiAlternatives(
            subject="ITQ Test",
            to=['email@email.com']
        )
        itq_html_body = render_to_string("initial_screening/itq_email.html", itq_email_template_context("My id", "This is my troubling experience", sample_response()))
        itq_email.attach_alternative(itq_html_body, "text/html")
        itq_email.send(fail_silently=False)
    if False:
        # send dass21 email
        dass21_html_body = render_to_string("initial_screening/dass21_email.html", dass21_email_context("This is my client id", dass21_sample_response()))
        dass21_email_ = EmailMultiAlternatives(
            subject="Dass21 Sample",
            to=['email@email.com']
        )
        dass21_email_.attach_alternative(dass21_html_body, "text/html")
        dass21_email_.send(fail_silently=False)

    context = dass21_email_context("client id", dass21_sample_response())
    return render(request, "initial_screening/dass21_email.html", context)

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
      "total_score": score.total
    }

    return context