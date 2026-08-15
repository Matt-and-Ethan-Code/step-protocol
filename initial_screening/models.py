from django.db import models
from django.db.models import ForeignKey, Q
from clinician_overview.models import Client

class Form(models.Model):
    """
    A whole area that a questionnaire can appear, ie Intake vs Post Exam vs Feedback form reference.
    So this is like the whole "initial screening" questionnaire, which contains the DES-T, PCL-5, etc.
    Like one big bundle of questionnaires.
    Contains only the questionnaire data, not the responses associated (only the shape of the data.)
    """
    id: int
    name = models.CharField(
        max_length=300, 
        unique=True, 
        help_text="The name of the form. This is for internal use only and will not be shown to the user.")
    anonymous = models.BooleanField(
        default=False, 
        help_text="If the form is anonymous, STEP will not display user answers to the clinician. There is no enforcement as to whether a question collecting user identity has been added."
        )

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
    omit_notifications = models.BooleanField(null=True, blank=True)
    hide_title = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class FormMembership(models.Model):
    """
    Tracks when a questionnaire belongs to a form.
    Also, tracks which order the questionnaire is in the form.
    Examples: 
        - STEP Into Page belongs to Initial Screening and Pre and Post Screening, and comes 
        first (Order = 1) in both
        - DES-T belongs to Initial Screening and comes second (Order = 2)

    Note: 
        - A questionnaire can belong to multiple forms
        - A questionnaire may also not belong to a form (although that wouldn't make sense, because then it 
        won't show up for the users).
    """
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    order = models.PositiveBigIntegerField(default=0)

    # Enforces that a questionnaire may belong to a form at most once 
    # Example:
    #   if a row has questionnaire = X and form = Y
    #   then no other row may have questionnaire = X and form = Y
    #   - On the other hand: 
    #       - A row where questionnaire = X and form = Z would be fine
    class Meta: 
        unique_together = [['questionnaire', 'form']]


class QuestionnaireResponse(models.Model):
    """
    Records that the user has entered a response for a form.
    -   Does not contain what the user entered
    -   To see what the user entered: see ResponseItem
    """
    user_identifier = ForeignKey(Client, on_delete=models.CASCADE, null=True) 
    form = ForeignKey(Form, on_delete=models.CASCADE)
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
        ('date', "Date"), 
        ('file', 'File')
    ]
    options: models.Manager["AnswerOption"]

    question_block = models.ForeignKey(
        QuestionBlock,
        related_name='questions',
        on_delete=models.CASCADE
    )

    text = models.TextField(max_length=1000, null=True, blank=True)
    question_type = models.CharField(
        max_length=30,
        choices=QUESTION_TYPES,
        default='text'
    )
    order = models.PositiveBigIntegerField(default=0)
    is_required = models.BooleanField(default=False)
    image_url = models.TextField(blank=True, null=True, help_text="Optional URL for an image to display with the question.")

    class Meta:
        ordering = ['order']
        constraints = [
            models.CheckConstraint(
                condition=Q(text__isnull=False) | Q(image_url__isnull=False), 
                name='not_both_image_and_question_text_null'
            )
        ]

    def __str__(self):
        thisText = self.text if self.text else ""
        displayText = thisText[:60] + "..." if len(thisText) > 60 else thisText

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
    internal_value = models.CharField(max_length=255,  null=True, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text


def document_upload_path(instance, filename):
    return f'documents/{instance.pk}/{filename}'

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
    file = models.FileField(upload_to=document_upload_path, null=True, blank=True)

