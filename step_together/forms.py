from typing import Any
from django import forms
from .models import Agreement


class AgreementForm(forms.Form):
    def __init__(self, *args: Any, agreement: Agreement, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.agreement = agreement
        self.text_questions = list(agreement.textquestion_set.order_by('id'))  # type: ignore[attr-defined]
        self.conditions = list(agreement.agreementcondition_set.order_by('id'))  # type: ignore[attr-defined]
        self.field_numbers: dict[str, int] = {}

        for question in self.text_questions:
            name = f'text_question_{question.id}'
            self.fields[name] = forms.CharField(
                label=question.question_text,
                max_length=200
            )
            self.field_numbers[name] = len(self.field_numbers) + 1

        for condition in self.conditions:
            name = f'condition_{condition.id}'
            self.fields[name] = forms.BooleanField(
                label=condition.confirmation_checkbox_text,
                required=True,
            )
            self.field_numbers[name] = len(self.field_numbers) + 1

        for field in self.fields.values():
            if field.required:
                field.label_suffix = ' <span class="required-label">(required)</span>'
            else:
                field.label_suffix = ""

    def get_text_answers(self) -> list[str]:
        return [self.cleaned_data[f'text_question_{question.id}'] for question in self.text_questions]
