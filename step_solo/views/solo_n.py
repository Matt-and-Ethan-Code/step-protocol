from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from step_solo.util.get_video_url import get_video_url
from step_solo.util.identified import solo_session_required


def solo_n(n: int):
    assert 3 <= n <= 11
    assert n != 8
    video_name = f'solo_{n}'
    previous_url = f"solo_{n - 1}"
    next_url = f"solo_{n + 1}"
    if n == 7:
        next_url = 'solo_8p1'
    if n == 9:
        previous_url = 'solo_8p2'

    @solo_session_required()
    def handler(request: HttpRequest) -> HttpResponse:
        ctx = {
            "title": f"Solo {n}",
            "video_url": get_video_url(video_name),
            "previous_url": previous_url,
            "next_url": next_url,
            "text": texts[n]
        }
        return render(request, f"step_solo/solo_n.html", context=ctx)

    return handler


texts = {
    3: "Let’s continue developing your resource or asset. Follow along with this video to complete the next steps.",
    4: "Now, let’s review the next step in the process. In this video, we’ll explain what to expect and demonstrate how the process works. For now, simply watch and listen—you don’t need to do anything yet. After this video, we’ll guide you step by step as you identify and begin to distance the disturbance.",
    5: "Now, we’ll begin by identifying your first Point of Disturbance (PoD). Take your time as you continue tapping back and forth on your worksheet. When a PoD comes to mind, write or draw it in the PoD 1 box.",
    6: "Let’s continue working with PoD 1. We’ll now process your first Point of Disturbance together.",
    7: "Now, we’ll scan for any remaining disturbance. Take your time as you continue tapping back and forth on your worksheet. When another PoD comes to mind, write or draw it in the PoD 2 box.",
    9: "If a third PoD came to mind, continue with this video to process it. Once processing is complete, or if there is no remaining disturbance, continue to the next video to complete STEP 6.",
    10: "Now, let’s begin Step 6. You’ll rate how disturbing the entire experience feels for you at this point. Complete this step after you have finished processing the PoDs you identified in Step 5. This step is completed even if you did not identify a third PoD.",
    11: "Take a moment to connect with the positive thought you identified and then complete a short set of butterfly hugs.",
    
}
