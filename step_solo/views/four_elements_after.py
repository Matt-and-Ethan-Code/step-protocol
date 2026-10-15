from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from step_solo.util.identified import solo_session_required
from step_solo.util import form_tokens as tok
from step_solo.util.get_video_url import get_video_url
from step_solo.models import SoloResponse
import clinician_overview.util.client as clientm
from typing import Literal

import urllib.parse

@solo_session_required()
def four_elements_after(request: HttpRequest) -> HttpResponse:
  if request.POST: return four_elements_after_post(request)
  else: return four_elements_after_get(request)

def four_elements_after_get(request: HttpRequest) -> HttpResponse:
  # TODO: check for error in the queryparams
  ctx = {
    "title": "The 4 Elements",
    "video_url": get_video_url('4_elements_without_music'),
    "previous_url": "solo_container",
    "next_url": "solo_complete",
  }
  return render(request, "step_solo/four_elements_after.html", context=ctx)

def nonnull[T](thing: T | None) -> T:
    assert not (thing is None)
    return thing

def four_elements_after_post(request: HttpRequest) -> HttpResponse:
  errors = []
  def err(tag: str):
    errors.append(tag)
  client_id = expect_str(request, tok.CLIENT_ID_TOKEN)
  if client_id is None: err("Client Identifier")

  provider_email = expect_str(request, tok.PROVIDER_EMAIL_TOKEN)
  if provider_email is None: err("Provider Email")
  stress_before_elements = expect_0to10(request, tok.STRESS_BEFORE_TOKEN)
  if stress_before_elements is None: err("Stress Before 4 Elements")
  stress_after_elements = expect_0to10(request, tok.STRESS_AFTER_TOKEN)
  if stress_after_elements is None: err("Stress After 4 Elements")
  step_2 = expect_0to10(request, tok.STEP_2_TOKEN)
  if step_2 is None: err("STEP 2")
  step_5pod1first = expect_0to10(request, tok.STEP_5_POD_1_TOKEN)
  if step_5pod1first is None: err("STEP 5 - PoD 1 First")
  step_5pod1last = expect_0to10(request, tok.STEP_5_POD_1_LAST_TOKEN)
  if step_5pod1last is None: err("STEP 5 - PoD 1 Last")
  step_5pod2first = expect_0to10(request, tok.STEP_5_POD_2_TOKEN)
  if step_5pod2first is None: err("STEP 5 - PoD 2 First")
  step_5pod2last = expect_0to10(request, tok.STEP_5_POD_2_LAST_TOKEN)
  if step_5pod2last is None: err("STEP 5 - PoD 2 Last")
  step_5pod3first = expect_0to10(request, tok.STEP_5_POD_3_TOKEN)
  if step_5pod3first is None: err("STEP 5 - PoD 3 First")
  step_5pod3last = expect_0to10(request, tok.STEP_5_POD_3_LAST_TOKEN)
  if step_5pod3last is None: err("STEP 5 - PoD 3 Last")
  step_6 = expect_0to10(request, tok.STEP_6_TOKEN)
  if step_6 is None: err("STEP 6")

  if len(errors) > 0:
    # put all errors in the queryparams
    query_params = { "errors": errors }
    base_url = reverse('solo_four_elements_after')
    query_string = urllib.parse.urlencode(query_params, doseq=True)
    return redirect(f"{base_url}?{query_string}")

  # should exist 100% since the @solo_session_required() guard would catch it otherwise
  client = nonnull(clientm.find(nonnull(client_id), nonnull(provider_email)))
  
  response = SoloResponse(
    client=client,
    stress_before_elements=nonnull(stress_before_elements),
    stress_after_elements=nonnull(stress_after_elements),
    step_2=nonnull(step_2),
    step_5pod1_first=nonnull(step_5pod1first),
    step_5pod1_last=nonnull(step_5pod1last),
    step_5pod2_first=nonnull(step_5pod2first),
    step_5pod2_last=nonnull(step_5pod2last),
    step_5pod3_first=nonnull(step_5pod3first),
    step_5pod3_last=nonnull(step_5pod3last),
    step_6=nonnull(step_6)
  )
  response.save()

  return redirect("solo_complete")

def expect_str(req: HttpRequest, token: str) -> str | None:
  maybe_str = req.session.get(token)
  if maybe_str is None: return None
  if isinstance(maybe_str, str):
    return maybe_str
  return None

def expect_0to10(req: HttpRequest, token: str) -> Literal[0,1,2,3,4,5,6,7,8,9,10] | None:
  maybe_int = req.session.get(token)
  if maybe_int is None: return None
  if isinstance(maybe_int, int) and maybe_int in (0,1,2,3,4,5,6,7,8,9,10):
    return maybe_int
  return None

