from django import forms
from django.utils.safestring import mark_safe
from typing import Any

from initial_screening.models import Questionnaire
    
class InfoWidget(forms.Widget):
    def render(self, name: str, value: Any, attrs: dict[str, Any] | None=None, renderer: Any | None =None):
        html = f'<div class="form-info">{self.attrs.get("text", "")}</div>'
        return mark_safe(html)


class InfoField(forms.Field):
    widget=InfoWidget

    def __init__(self, text:str="", *args:Any, **kwargs:Any):
        kwargs['required'] = False
        super().__init__(*args, **kwargs)
        self.text = text

    def clean(self, value: Any):
        return None 

class QuestionnaireForm(forms.Form):
    def __init__(self, questionnaire: Questionnaire, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.questionnaire = questionnaire

        for block in questionnaire.question_blocks.all():
            for question in block.questions.all():
                field_name = f"question_{question.id}"

                if question.question_type == 'text':
                    self.fields[field_name] = forms.CharField(
                        label=question.text,
                        required=question.is_required,
                        widget=forms.TextInput(attrs={'class':'text-input'})
                    )

                elif question.question_type == 'info':
                    self.fields[field_name] = InfoField(
                        text=question.text, 
                        label='',
                        widget=InfoWidget(attrs={'text': question.text})
                    )
                    
                elif question.question_type == 'dropdown':
                    choices = [(opt.id, opt.text) for opt in question.options.all()]

                    self.fields[field_name] = forms.ChoiceField(
                        label=question.text,
                        choices=choices,
                        required=question.is_required,
                        widget=forms.Select(attrs={'class':'dropdown-select'})
                    )
                elif question.question_type == 'radio':
                    choices = [(opt.id, opt.text) for opt in question.options.all()]
                    self.fields[field_name] = forms.ChoiceField(
                        label=question.text,
                        choices=choices,
                        required=question.is_required,
                        widget=forms.RadioSelect
                    )
