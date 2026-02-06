from django.db import models
from django.db.models import ForeignKey

class Questionnaire(models.Model):
    name = models.CharField(max_length=300, unique=True)
    citation = models.TextField(blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveBigIntegerField(default=0,unique=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
class QuestionnaireResponse(models.Model):
    user_identifier = models.CharField(max_length=300, null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0, null=False)
    """The number of times a clinician has viewed the response."""
class QuestionBlock(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire,
        related_name='question_blocks',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        if self.title:
            return f"{self.questionnaire.name}: {self.title}"
        return f"{self.questionnaire.name} (Untitled Block)"


class Question(models.Model):
    QUESTION_TYPES = [
        ('info', "Informational Block"),
        ('text', "Single Line Text"),
        ("textarea", "Long Text"),
        ('radio', "Multiple Choice (Single-select)"),
        ('checkbox', "Multiple Choice (Multi-select)"),
        ('dropdown', "Dropdown"),
        ('date', "Date")
    ]

    question_block = models.ForeignKey(
        QuestionBlock,
        related_name='questions',
        on_delete=models.CASCADE
    )

    text = models.TextField(max_length=1000)
    question_type = models.CharField(
        max_length=30,
        choices=QUESTION_TYPES,
        default='text'
    )
    order = models.PositiveBigIntegerField(default=0)
    is_required = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        displayText = self.text[:60] + "..." if len(self.text) > 60 else self.text

        return displayText

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveBigIntegerField(default=0)
    internal_value = models.CharField(max_length=255,  null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text

class ResponseItem(models.Model):
    response: ForeignKey[QuestionnaireResponse] = models.ForeignKey(QuestionnaireResponse, related_name='items', on_delete=models.CASCADE)
    question: ForeignKey[Question] = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    answerID = models.ForeignKey(AnswerOption, null=True, blank=True, on_delete=models.SET_NULL)