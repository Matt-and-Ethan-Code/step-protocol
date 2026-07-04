from django.db import models

# represents an instance of provider having filled out an agreement form.
# stores the two text fields that they entered (name & organization)
# they also would've filled checkboxes acknowledging the terms of the agreement
# check the Agreement model for the content of those terms
# use the agreement date to find the correct version
class ProviderConfirmation(models.Model):
    provider_name = models.CharField(max_length=100)
    provider_organization = models.CharField(max_length=100)
    agreement_date = models.DateTimeField(auto_now_add=True)
    agreement = models.ForeignKey('Agreement', on_delete=models.CASCADE)  # type: ignore[type-arg]

# represents an instance of the agreement
class Agreement(models.Model):
    # the date when this agreement was tweaked
    # example: adding terms, tweaking wording, etc.
    agreement_version_date = models.DateTimeField(auto_now_add=True)
    # the text questions the user must fill (name, organization)
    current = models.BooleanField(default=True)

class TextQuestion(models.Model):
    question_text = models.TextField()
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)  # type: ignore[type-arg]

class AgreementCondition(models.Model):
    condition_text = models.TextField()
    confirmation_checkbox_text = models.TextField()
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)  # type: ignore[type-arg]
