from django.db import models
from django.contrib.auth.models import User

class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_questionnaire = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Questionnaire {self.current_questionnaire}"

class QuestionnaireResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey('Questionnaire', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

class ResponseItem(models.Model):
    response = models.ForeignKey(QuestionnaireResponse, related_name='items', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.TextField()

class Questionnaire(models.Model):
    name = models.CharField(max_length=300, unique=True)
    citation = models.TextField(blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveBigIntegerField(default=0,unique=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
    
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
        return f"[{self.question_block.title or self.question_block.questionnaire.name}] {self.text}"

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text