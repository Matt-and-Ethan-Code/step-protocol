from django.db import models

class Questionnaire(models.Model):
    name = models.CharField(max_length=300, unique=True)
    citation = models.TextField(blank=True)

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
        ('text', "Single Line Text"),
        ("textarea", "Long Text"),
        ('radio', "Multiple Choice (Single-select)"),
        ('checkbox', "Multiple Choice (Multi-select)"),
        ('rating', "Rating (Stars or Scale)"),
        ('dropdown', "Dropdown"),
        ('date', "Date"),
        ('info', "Informational Block")
    ]

    question_block = models.ForeignKey(
        QuestionBlock,
        related_name='questions',
        n_delete=models.CASCADE
    )

    text = models.CharField(max_length=500)
    question_type = models.CharField(
        max_length=30,
        choices=QUESTION_TYPES,
        default='text'
    )
    order = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"[{self.question_block.title or self.block.questionnaire.name}] {self.text}"

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.text} (weight={self.weight})"