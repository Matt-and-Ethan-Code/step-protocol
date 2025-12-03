from django.core.management.base import BaseCommand 
from django.core.management import call_command
from initial_screening.models import Questionnaire, QuestionBlock, Question, AnswerOption

class Command(BaseCommand):
    help = "Seed the database with questionnaire data"

    def handle(self, *args, **options):
        AnswerOption.objects.all().delete()
        Question.objects.all().delete()
        QuestionBlock.objects.all().delete()
        Questionnaire.objects.all().delete()

        self.stdout.write("Deleted all old data.")

        call_command('loaddata', 'questionnaire.json')
        self.stdout.write("Loaded questionnaire data.")

        call_command('loaddata', 'questionblock.json')
        self.stdout.write("Loaded question block data.")

        call_command('loaddata', 'question.json')
        self.stdout.write("Loaded question data.")

        call_command('loaddata', 'answeroption.json')
        self.stdout.write("Loaded answer option data.")
