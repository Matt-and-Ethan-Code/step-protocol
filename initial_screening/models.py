from django.db import models
from django.db.models import ForeignKey
from clinician_overview.models import ClientId

class Form(models.Model):
    """
    A whole area that a questionnaire can appear, ie Intake vs Post Exam vs Feedback form reference.
    So this is like the whole "initial screening" questionnaire, which contains the DES-T, PCL-5, etc.
    Like one big bundle of questionnaires.
    Contains only the questionnaire data, not the responses associated (only the shape of the data.)
    """
    id: int
    name = models.CharField(max_length=300, unique=True)

class Questionnaire(models.Model):
    """
    A set of questions, like the DES-T. A questionnaire always appears on one page.
    In the initial screening, each time you click 'Next' to go to the next page it is another
    questionnaire object.
    Contains references to the questions (QuestionBlock) but not the actual responses (that's QuestionnaireReponse).
    """
    id: int
    name = models.CharField(max_length=300, unique=True)
    citation = models.TextField(blank=True)
    description = models.TextField(blank=True)
    question_blocks: models.Manager["QuestionBlock"]

    def __str__(self):
        return self.name
    
class FormMembership(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    order = models.PositiveBigIntegerField(default=0)

    class Meta: 
        unique_together = [['questionnaire', 'form', 'order']]


class QuestionnaireResponse(models.Model):
    user_identifier = ForeignKey(ClientId, on_delete=models.CASCADE) #models.CharField(max_length=300, null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0, null=False)
    """The number of times a clinician has viewed the response."""

class QuestionBlock(models.Model):
    """
    In a questionnaire, sometimes there is a little section like "for the next 3 questions, think about how often
    it has occurred in the past month". A QuestionBlock is a set of questions that is logically grouped like that and
    it is stored in the Questionnaire and "normal" questions are just in one big QuestionBlock.
    """
    questionnaire = models.ForeignKey(
        Questionnaire,
        related_name='question_blocks',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    questions: models.Manager["Question"]

    class Meta:
        ordering = ['order']

    def __str__(self):
        if self.title:
            return f"{self.questionnaire.name}: {self.title}"
        return f"{self.questionnaire.name} (Untitled Block)"


class Question(models.Model):
    id: int

    QUESTION_TYPES = [
        ('info', "Informational Block"),
        ('text', "Single Line Text"),
        ("textarea", "Long Text"),
        ('radio', "Multiple Choice (Single-select)"),
        ('checkbox', "Multiple Choice (Multi-select)"),
        ('dropdown', "Dropdown"),
        ('date', "Date")
    ]
    options: models.Manager["AnswerOption"]

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
    """
    For multiple choice questions. Each question has their own set of AnswerOptions (ie, each is like "Extremely Often", "Somewhat Often").
    internal_value is for the special case where you select a provider by name but you want the actual value to be their email (the user sees one thing
    and inside its something else).
    Text questions do not have an AnswerOption
    """
    id: int
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveBigIntegerField(default=0)
    internal_value = models.CharField(max_length=255,  null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text

class ResponseItem(models.Model):
    """
    The response a user provides for an individual question. (For the full questionnaire, look at QuestionnaireResponse).
    The answer field will probably always be present, mostly for convenience. If you are a text field, it contains the text
    that the user entered. If it is a multiple choice question, it'll be the text of the option they clicked on (ie, 'Somewhat Likely'). Otherwise
    it is blank.
    The answerID is more what the code should be using (especially for multiple choice). It is the actual option that the user picked in the DB.
    """
    response: ForeignKey[QuestionnaireResponse] = models.ForeignKey(QuestionnaireResponse, related_name='items', on_delete=models.CASCADE)
    question: ForeignKey[Question] = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    answerID = models.ForeignKey(AnswerOption, null=True, blank=True, on_delete=models.SET_NULL)