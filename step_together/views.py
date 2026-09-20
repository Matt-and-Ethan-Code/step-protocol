from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from initial_screening.decorators.clinician_decorator import clinician_required
from step_solo.util.get_video_url import get_video_url
from dataclasses import dataclass
from typing import Literal

from .forms import AgreementForm
from .models import Agreement, AgreementCondition, ProviderConfirmation

@dataclass
class ST_MODULE:
    title: str
    img_url: str
    description: str
    page_url: str

@dataclass
class ST_MODULE_CONTAINER:
    title: str
    modules: list[ST_MODULE]


step_together_content_modules = ST_MODULE_CONTAINER(
        title="STEP Together Protocol", 
        modules=[
            ST_MODULE(
                title="Welcome to STEP Together", 
                img_url="step_together/images/step-together-welcome-thumbnail.jpeg",
                description="⭐Refer to the script for detailed guidance throughout the protocol. Key points will be brief...", 
                page_url="/step-together/welcome-to-step-together"
            ), 
            ST_MODULE(
                title="STEP Self-Care Introduction", 
                img_url="step_together/images/step-together-introduction-thumbnail.jpeg", 
                description="Leaders - please read the text below to your participants. Let's watch the first video with a sh...", 
                page_url="/step-together/self-care-introduction"
            ), 
            ST_MODULE(
                title="Bilateral Tapping", 
                img_url="step_together/images/step-together-bilateral-tapping-thumbnail.jpeg",
                description="Leaders - please read the text below to your participants. Next, is the Four Elements Video. The...", 
                page_url="/step-together/bilateral-tapping"
            ), 
            ST_MODULE(
                title="4 Elements", 
                img_url="step_together/images/step-together-4-elements-thumbnail.jpeg", 
                description="Leaders - please read the text below to your participants. Ensure you are in a comfortable locat...", 
                page_url="/step-together/4-elements"
            ), 
            ST_MODULE(
                title="Check-In", 
                img_url="step_together/images/step-together-check-in-thumbnail.jpeg", 
                description="Leaders - please read the text below to your participants. Please send us your 0 to 10 ratings B...", 
                page_url="/step-together/check-in"
            ), 
            ST_MODULE(
                title="STEP Together Protocol Sheet", 
                img_url="step_together/images/step-together-protocol-thumbnail.jpeg", 
                description="⭐Re-introduce your team, conduct a technology check, and ensure participants have all the needed...", 
                page_url="/step-together/protocol-sheet"
            ), 
            ST_MODULE(
                title="Check-In", 
                img_url="step_together/images/step-together-check-in-thumbnail.jpeg", 
                description="Leaders - please read the text below to your participants. What are you taking with you from the...", 
                page_url="/step-together/check-in-pt-2"
            ), 
            ST_MODULE(
                title="The Container",
                img_url="step_together/images/step-together-container-thumbnail.jpeg",
                description="Leaders - please read the text below to your participants. Let's do the container activity toget...", 
                page_url="/step-together/container"
            ), 
            ST_MODULE(
                title="4 Elements",
                img_url="step_together/images/step-together-4-elements-thumbnail.jpeg", 
                description="Leaders - please read the text below to your participants. Let's take 10 minutes now before we e...", 
                page_url="/step-together/4-elements-pt-2"
            ), 
            ST_MODULE(
                title="Ending", 
                img_url="step_together/images/step-together-ending-thumbnail.jpeg", 
                description="Leaders - please read the text below to your participants. We would like you to take a moment aft...", 
                page_url="/step-together/ending"
            )
        ]
    )

step_together_modules:list[ST_MODULE_CONTAINER] = [
    ST_MODULE_CONTAINER(
        title="STEP Together Clinician Agreement",
        modules=[
            ST_MODULE(
                title = "STEP Together Clinician Agreement", 
                img_url = "step_together/images/step-together-agreement-thumbnail.jpeg",
                description = "Self-Care Traumatic Episode Protocol (STEP) Agreement For STEP Intervention Providers", 
                page_url="/step-together/past-agreement/"
            )
        ]
    ), 
    ST_MODULE_CONTAINER(
        title="STEP Together Manual", 
        modules=[
            ST_MODULE(
                title = "Manual", 
                img_url = "step_together/images/step-together-manual-thumbnail.jpeg", 
                description = "Please review the manual carefully before you begin planning your first STEP Together group. It ...", 
                page_url="/clinician/resources"
            )
        ]
    ), 
    ST_MODULE_CONTAINER(
        title="Before the Group", 
        modules=[
            ST_MODULE(
                title="STEP Together Pre-Group Checklist, Materials & Forms", 
                img_url = "step_together/images/step-together-checklist-thumbnail.jpeg", 
                description = "Below, you will find everything you will need before beginning your first STEP Together group. Pl...", 
                page_url="/step-together/pregroup-checklist"
            )
        ]
    ), 
    step_together_content_modules, 
    ST_MODULE_CONTAINER(
        title="After the Group", 
        modules=[
            ST_MODULE(
                title="After the Group", 
                img_url="step_together/images/step-together-checklist-thumbnail.jpeg", 
                description="After the group, please remember to: Pre-and-Past-Data Forms: Those eligible for the STEP Toget...", 
                page_url="/step-together/post-group-checklist"
            )
        ]
    )
]

@clinician_required
def step_together_portal_view(request: HttpRequest) -> HttpResponse:
    return render(request, "step_together/step-together.html", {
        "nav_section": "step-together", 
        "modules": step_together_modules
    })

@clinician_required
def step_together_manual(request: HttpRequest) -> HttpResponse:
    return render(request, "step_together/step-together-manual.html", 
        {"content_links": [
            {"icon": "step_together/acrobat.png", 
             "url": 'clinician_overview/STEP_Manual.pdf', 
             "name": "STEP_Manual_Updated_December_2025_.pdf"}, 
             {"icon": 'step_together/acrobat.png', 
              "url": 'clinician_overview/STEP_Script.pdf', 
              "name": "STEP_Script.pdf"
             }
             ], 
            "next_link": "/step-together/pregroup-checklist"
            })

@clinician_required
def step_together_pregroup_checklist(request: HttpRequest) -> HttpResponse:
    return render(request, "step_together/step-together-pre-group-checklist.html", 
                  {
                      "next_link": '/step-together/welcome-to-step-together/', 
                      "prev_link": '/step-together/manual/'
                  })

@clinician_required
def welcome_to_step_together(request: HttpRequest) -> HttpResponse:
    return render(request, "step_together/welcome-to-step-together.html", {
        "nav_section": "step-together", 
        "scrollbar": step_together_content_modules,
        'this_content_index': 0, 
        "content_links": [
            {
                "icon": 'step_together/acrobat.png', 
                "url": 'clinician_overview/STEP_Script.pdf', 
                "name": "STEP_Script.pdf"
            }
        ], 
        "next_link": '/step-together/self-care-introduction/',
        "prev_link": '/step-together/pregroup-checklist/'
    })

@clinician_required
def self_care_introduction(request:HttpRequest) -> HttpResponse:
    return render(request, "step_together/self-care-introduction.html", {
        "video_url": get_video_url('st_self_care_introduction'), 
        "scrollbar": step_together_content_modules, 
        'this_content_index': 1,
        "next_link": '/step-together/bilateral-tapping/',
        "prev_link": '/step-together/welcome-to-step-together/'
    })

@clinician_required
def bilateral_tapping(request:HttpRequest) -> HttpResponse: 
    return render(request, 'step_together/bilateral-tapping.html', {
        'video_url': get_video_url('st_bilateral_tapping'), 
        "scrollbar": step_together_content_modules, 
        'this_content_index': 2, 
        "next_link": '/step-together/4-elements/', 
        'prev_link': '/step-together/self-care-introduction/'
    })

@clinician_required
def four_elements_pt1(request:HttpRequest) -> HttpResponse: 
    return render(request, 'step_together/four-elements-pt1.html', {
        'video_url': get_video_url('st_4_elements'), 
        "scrollbar": step_together_content_modules, 
        'this_content_index': 3, 
        'next_link': '/step-together/check-in/', 
        'prev_link': '/step-together/bilateral-tapping/'
    })

@clinician_required
def check_in(request:HttpRequest) -> HttpResponse: 
    return render(request, 'step_together/check-in.html', {
        "scrollbar": step_together_content_modules, 
        'this_content_index': 4, 
        'next_link': '/step-together/protocol-sheet/', 
        'prev_link': '/step-together/4-elements/'
    })

@clinician_required
def step_together_protocol_sheet(request:HttpRequest) -> HttpResponse:
    return render(request, 'step_together/step-together-protocol-sheet.html', {
        'video_url': get_video_url('st_protocol_sheet'), 
        "scrollbar": step_together_content_modules, 
        'this_content_index': 5, 
        'next_link': '/step-together/check-in-pt-2', 
        'prev_link': '/step-together/check-in/'
    })

@clinician_required
def check_in2(request:HttpRequest) -> HttpResponse:
    return render(request, 'step_together/check-in-2.html', {
        'scrollbar': step_together_content_modules, 
        'this_content_index': 6, 
        'next_link': '/step-together/container', 
        'prev_link': '/step-together/protocol-sheet/'
    })

@clinician_required
def container(request:HttpRequest) -> HttpResponse:
    return render(request, 'step_together/container.html', {
        'video_url': get_video_url('st_container'), 
        'scrollbar': step_together_content_modules, 
        'this_content_index': 7, 
        'next_link': '/step-together/4-elements-pt-2', 
        'prev_link': '/step-together/check-in-pt-2'
    })

@clinician_required
def four_elements_pt2(request:HttpRequest) -> HttpResponse:
    return render(request, 'step_together/four-elements-pt2.html', {
        'video_url': get_video_url('st_4_elements_pt2'), 
        'scrollbar': step_together_content_modules, 
        'this_content_index': 8, 
        'next_link': '/step-together/ending', 
        'prev_link': '/step-together/container'
    })

@clinician_required
def ending(request:HttpRequest) -> HttpResponse:
    return render(request, 'step_together/ending.html', {
        'scrollbar': step_together_content_modules, 
        'this_content_index': 9, 
        'prev_link': '/step-together/4-elements-pt-2' 
    })

@clinician_required
def post_group_checklist(request:HttpRequest) -> HttpResponse:
    return render(request, 'step_together/step-together-post-group-checklist.html')

@clinician_required
def past_agreement_view(request: HttpRequest) -> HttpResponse:
    confirmation = get_object_or_404(ProviderConfirmation, provider=request.user)
    agreement = get_object_or_404(Agreement, id=confirmation.agreement.id)
    agreement_conditions = AgreementCondition.objects.filter(agreement=agreement)
    print("condition: ", agreement_conditions)
    return render(request, "step_together/past-agreement.html", {
        'confirmation': confirmation,
        "conditions": agreement_conditions,
        'nav_section': 'step-together'
    })

@clinician_required
def agreement_view(request: HttpRequest) -> HttpResponse:
    agreement = get_object_or_404(Agreement, current=True)

    if request.method == "POST":
        form = AgreementForm(request.POST, agreement=agreement)
        if form.is_valid():
            # by convention the first text question is the provider's name
            # and the second is their organization (see ProviderConfirmation)
            answers = form.get_text_answers()
            provider_name = answers[0] if len(answers) > 0 else ""
            provider_organization = answers[1] if len(answers) > 1 else ""

            ProviderConfirmation.objects.create(
                provider=request.user,
                provider_name=provider_name,
                provider_organization=provider_organization,
                agreement=agreement,
            )
            return redirect("notifications")  
    else:
        form = AgreementForm(agreement=agreement)

    return render(request, "step_together/agreement.html", {
        "form": form,
        "agreement": agreement,
        'nav_section': 'step-together'
    })