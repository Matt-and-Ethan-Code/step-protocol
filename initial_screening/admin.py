from django.contrib import admin
import nested_admin

from .models import Questionnaire, QuestionBlock, Question, AnswerOption, QuestionnaireResponse, ResponseItem, Form, FormMembership

class AnswerOptionInline(nested_admin.NestedTabularInline): # type: ignore[type-arg]
    model = AnswerOption
    extra = 0

class QuestionInline(nested_admin.NestedTabularInline): # type: ignore[type-arg]
    model = Question
    show_change_link = True
    extra = 0
    inlines = [AnswerOptionInline]

class QuestionBlockInline(nested_admin.NestedTabularInline): # type: ignore[type-arg]
    model = QuestionBlock
    show_change_link = True
    extra = 0
    inlines = [QuestionInline]

class ResponseItemInline(admin.TabularInline): # type: ignore[type-arg]
    model = ResponseItem
    extra = 0

class QuestionnaireInline(nested_admin.NestedTabularInline): # type: ignore[type-arg]
    model = Questionnaire
    extra = 0

class FormMembershipInline(nested_admin.NestedTabularInline): # type: ignore[type-arg]
    model = FormMembership
    extra = 0

@admin.register(Form)
class FormAdmin(nested_admin.NestedModelAdmin): # type: ignore[type-arg]
    list_display = ('name','anonymous','questionnaires')
    inlines = [FormMembershipInline]

    @admin.display(description='Questionnaires')
    def questionnaires(self, obj):
        return ', '.join(
            obj.formmembership_set.order_by('order').values_list('questionnaire__name', flat=True)
        )

@admin.register(QuestionnaireResponse)
class QuestionnaireResponseAdmin(admin.ModelAdmin): # type: ignore[type-arg]
    list_display = ('user_identifier', 'questionnaire', 'submitted_at')
    list_filter = ('user_identifier', 'questionnaire', 'submitted_at')
    inlines = [ResponseItemInline]

# main interface for creating and managing questionnaires.
@admin.register(Questionnaire)
class QuestionnaireAdmin(nested_admin.NestedModelAdmin): # type: ignore[type-arg]
    list_display = ('name', 'citation', 'description', 'omit_notifications')
    inlines = [QuestionBlockInline]

@admin.register(QuestionBlock)
class QuestionBlockAdmin(nested_admin.NestedModelAdmin): # type: ignore[type-arg]
    list_display = ('title', 'questionnaire', 'order', 'description')
    inlines = [QuestionInline]

# defines the Questions interface (table of all existing tables)
@admin.register(Question)
class QuestionAdmin(nested_admin.NestedModelAdmin): # type: ignore[type-arg]
    list_display = ('order', 'text', 'question_type', 'is_required', 'questionnaire', 'answer_options')
    list_filter = ('question_type', 'question_block__questionnaire')
    inlines = [AnswerOptionInline]

    # instructions for how to display the questionnaire field
    @admin.display(description='Questionnaire')
    def questionnaire(self, obj):
        return obj.question_block.questionnaire

    # instructions for how to display the answer options field
    @admin.display(description='Answer Options')
    def answer_options(self, obj):
        return ', '.join(obj.options.values_list('text', flat=True))
