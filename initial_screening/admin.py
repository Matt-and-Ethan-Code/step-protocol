from django.contrib import admin
from .models import Questionnaire, QuestionBlock, Question, AnswerOption, QuestionnaireResponse, ResponseItem

class AnswerOptionInline(admin.TabularInline): # type: ignore[type-arg]
    model = AnswerOption
    extra = 1

class QuestionInline(admin.TabularInline): # type: ignore[type-arg]
    model = Question
    extra = 1

class QuestionBlockInline(admin.TabularInline): # type: ignore[type-arg]
    model = QuestionBlock
    extra = 1

class ResponseItemInline(admin.TabularInline): # type: ignore[type-arg]
    model = ResponseItem
    extra = 0

@admin.register(QuestionnaireResponse)
class QuestionnaireResponseAdmin(admin.ModelAdmin): # type: ignore[type-arg]
    list_display = ('user_identifier', 'questionnaire', 'submitted_at')
    list_filter = ('user_identifier', 'questionnaire', 'submitted_at')
    inlines = [ResponseItemInline]
    


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin): # type: ignore[type-arg]
    list_display = ('name', 'citation', 'description', 'order')
    ordering=('order',)
    inlines = [QuestionBlockInline]

@admin.register(QuestionBlock)
class QuestionBlockAdmin(admin.ModelAdmin): # type: ignore[type-arg]
    list_display = ('title', 'questionnaire', 'order', 'description')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin): # type: ignore[type-arg]
    list_display = ('text', 'order', 'question_block', 'question_type', 'is_required', 'order')
    list_filter = ('question_type', 'question_block__questionnaire', 'question_block')
    inlines = [AnswerOptionInline]
