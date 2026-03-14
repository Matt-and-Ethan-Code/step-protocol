from django import template
from django import forms
from django.utils.safestring import mark_safe

register = template.Library()
@register.simple_tag 
def render_label(field: forms.BoundField):
    required_html = '<span class="required-label">(required)</span>' if field.field.required else ''
    html = f'<label for="{field.id_for_label}">{field.label} {required_html}</label>'
    return mark_safe(html)
