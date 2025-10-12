from django.contrib import admin
from .models import Questionnaire, QuestionBlock, Question, AnswerOption

class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuestionBlockInline(admin.TabularInline):
    model = QuestionBlock
    extra = 1

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('name', 'citation')
    inlines = [QuestionBlockInline]

@admin.register(QuestionBlock)
class QuestionBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'questionnaire', 'order', 'description')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_block', 'question_type', 'order')
    inlines = [AnswerOptionInline]
