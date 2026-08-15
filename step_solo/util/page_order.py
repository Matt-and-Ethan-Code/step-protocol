
from typing import Literal

from django.http import HttpRequest

type SoloPage = Literal['index', 'what_to_expect', 'self_regulation_strategies', 'getting_started', 'solo_introduction', 'bilateral_tapping', 'solo_intervention']

ORDER: list[SoloPage] = ['index', 'what_to_expect', 'self_regulation_strategies', 'getting_started', 'solo_introduction', 'bilateral_tapping', 'solo_intervention']


COMPLETED_SOLO_PAGES_COOKIE = 'solo_completed_pages'
def require_previous(req: HttpRequest, current_page: SoloPage) -> None:
    completed_pages: list[SoloPage] = req.session.get(COMPLETED_SOLO_PAGES_COOKIE, [])
    current_page_index = ORDER.index(current_page)
    
    
    

    
    
