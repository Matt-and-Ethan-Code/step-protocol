from django import forms
from django.contrib import admin, messages
from .models import Questionnaire, QuestionBlock, Question, AnswerOption, QuestionnaireResponse, ResponseItem, Form, FormMembership
from .validators import validate_sequential_order

class AnswerOptionInline(admin.TabularInline): # type: ignore[type-arg]
    model = AnswerOption
    extra = 1

class QuestionInline(admin.TabularInline): # type: ignore[type-arg]
    model = Question
    extra = 1
    show_change_link = True

class QuestionBlockInline(admin.TabularInline): # type: ignore[type-arg]
    model = QuestionBlock
    extra = 1
    show_change_link = True

class ResponseItemInline(admin.TabularInline): # type: ignore[type-arg]
    model = ResponseItem
    extra = 0

class QuestionnaireInline(admin.TabularInline): # type: ignore[type-arg]
    model = Questionnaire
    extra = 1

class FormMembershipInline(admin.TabularInline): # type: ignore[type-arg]
    model = FormMembership
    extra = 1

@admin.register(Form)
class FormAdmin(admin.ModelAdmin): # type: ignore[type-arg]
    list_display = ('name','anonymous')
    inlines = [FormMembershipInline]

@admin.register(QuestionnaireResponse)
class QuestionnaireResponseAdmin(admin.ModelAdmin): # type: ignore[type-arg]
    list_display = ('user_identifier', 'questionnaire', 'submitted_at')
    list_filter = ('user_identifier', 'questionnaire', 'submitted_at')
    inlines = [ResponseItemInline]

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin): # type: ignore[type-arg]
    list_display = ('name', 'citation', 'description', 'omit_notifications')
    inlines = [QuestionBlockInline]

@admin.register(QuestionBlock)
class QuestionBlockAdmin(admin.ModelAdmin): # type: ignore[type-arg]
    list_display = ('title', 'questionnaire', 'order', 'description')
    inlines = [QuestionInline]

class QuestionAdminForm(forms.ModelForm): # type: ignore[type-arg]
    class Meta:
        model = Question
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        question_block = cleaned_data.get('question_block')
        order = cleaned_data.get('order')
        if question_block is not None and order is not None:
            sibling_orders = list(
                Question.objects
                .filter(question_block=question_block)
                .exclude(pk=self.instance.pk)
                .values_list('order', flat=True)
            )
            validate_sequential_order(sibling_orders + [order], label="Question")
        return cleaned_data

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin): # type: ignore[type-arg]
    form = QuestionAdminForm
    list_display = ('order', 'text', 'question_type', 'is_required', 'question_block', 'questionnaire')
    list_filter = ('question_type', 'question_block__questionnaire', 'question_block')
    inlines = [AnswerOptionInline]

    @admin.display(description='Questionnaire')
    def questionnaire(self, obj):
        return obj.question_block.questionnaire
