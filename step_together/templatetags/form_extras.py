from django import template
from django import forms
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_question_number(field: forms.BoundField):
    number = field.form.field_numbers[field.name]  # type: ignore[attr-defined]
    return mark_safe(f'<div class="question-number">Question {number}</div>')

@register.simple_tag
def render_label(field: forms.BoundField):
    number = field.form.field_numbers[field.name]  # type: ignore[attr-defined]
    html = f'<label for="{field.id_for_label}">{field.label}</label>'
    return mark_safe(html)


@register.simple_tag
def text_question_field(form: forms.Form, question_id: int) -> forms.BoundField:
    return form[f'text_question_{question_id}']


@register.simple_tag
def condition_field(form: forms.Form, condition_id: int) -> forms.BoundField:
    return form[f'condition_{condition_id}']
