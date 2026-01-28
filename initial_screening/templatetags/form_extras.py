from django import template
from typing import Any

register = template.Library()

@register.filter 
def get_item(form: dict[Any, Any], key: Any):
    return form[key]