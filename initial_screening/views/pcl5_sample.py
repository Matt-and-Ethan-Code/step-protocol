from django.shortcuts import render
import initial_screening.scoring as scoring

def pcl5_sample() -> scoring.Pcl5Form:
  form: scoring.Pcl5Form = {
    1: 0,
    2: 0,
    3: 1,
    4: 0,
    5: 0,
    6: 0,
    7: 2,
    8: 0,
    9: 0,
    11: 3,
    12: 0,
    13: 0,
    14: 1,
    15: 0,
    16: 4,
    17: 0,
    18: 1,
    19: 0,
    20: 1,
  }
  return form

def pcl5_email_context(client_id: str, responses: scoring.Pcl5Form):
  pcl5_score = scoring.pcl5_score(responses)
  return {
    "client_id": client_id,
    "ptsd_indicated": pcl5_score.ptsd_indicated,
    "score": pcl5_score.score,
  }

def pcl5_email(request):
  context = pcl5_email_context("This is a client id", pcl5_sample())
  return render(request, "initial_screening/pcl5_email.html", context)