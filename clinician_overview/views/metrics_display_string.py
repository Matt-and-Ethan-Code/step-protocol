from django.template.loader import render_to_string
from clinician_overview.scoring.dest import DesTScore
from clinician_overview.scoring.dass21 import Dass21Score
from clinician_overview.scoring.gse import GSEScore
from clinician_overview.scoring.itq_dichotomous import ItqDichotomousScore
from clinician_overview.scoring.pcl5_diagnostic import Pcl5Score

def render_dest(score: DesTScore) -> str:
  print("score: ", score)
  return render_to_string("clinician_overview/detailed_form_result_display/dest_results.html", {"DEST": score})

def render_dass21(score: Dass21Score) -> str:
    return render_to_string("clinician_overview/detailed_form_result_display/dass21_results.html", {"DASS21": score})

def render_itq(itq_score: ItqDichotomousScore) -> str:
    return render_to_string("clinician_overview/detailed_form_result_display/itq_results.html", {"ITQ": itq_score})

def render_pcl5(pcl5_score: Pcl5Score) -> str:
    return render_to_string("clinician_overview/detailed_form_result_display/pcl5_results.html", {"PCL5": pcl5_score})

def render_gse(gse_score: GSEScore) -> str:
    return render_to_string("clinician_overview/detailed_form_result_display/gse_results.html", {"GSE": gse_score})   

