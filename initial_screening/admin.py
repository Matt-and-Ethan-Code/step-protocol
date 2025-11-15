from django.contrib import admin
from django.utils.html import format_html
from .models import Questionnaire, QuestionBlock, Question, AnswerOption, QuestionnaireResponse

class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuestionBlockInline(admin.TabularInline):
    model = QuestionBlock
    extra = 1

@admin.register(QuestionnaireResponse)
class QuestionnaireResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'questionnaire', 'submitted_at', 'formatted_responses')
    list_filter = ('questionnaire', 'submitted_at', 'user')
    


    def formatted_responses(self, obj):
        import json 
        formatted = json.dumps(obj.responses, indent=4, ensure_ascii=False)
        return format_html("<pre>{}</pre>", obj.responses)
    
    formatted_responses.short_description = "Responses"

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('name', 'citation', 'description', 'order')
    ordering=('order',)
    inlines = [QuestionBlockInline]

@admin.register(QuestionBlock)
class QuestionBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'questionnaire', 'order', 'description')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'order', 'question_block', 'question_type', 'is_required', 'order')
    inlines = [AnswerOptionInline]

    # class Media:
    #     js = ('admin/js/question_admin.js')
