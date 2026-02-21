from django import forms
from typing import Any
from .models import Provider

class ProviderIntakeForm(forms.ModelForm):
    class Meta:
        model = Provider 
        exclude=('user', )

    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        required=True
    )

    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        required=True
    )

    signup_news = forms.BooleanField(
        label="Sign up for news and updates", 
        required=False
    )

    scoring_email = forms.EmailField(
        label="Email for STEP Scoring Information", 
        required=True, 
        help_text="Please confirm the email address to which you would like the STEP scoring information to be sent. This should be a secure and confidential address where you are comfortable receiving client-related data."
    )

    phone_country_choices = [
            ("+61", "Australia"),
            ("+1", "Canada"),
            ("+64", "New Zealand"),
            ("+44", "United Kingdom"),
            ("+1", "United States"),
            ("+93", "Afghanistan"),
            ("+355", "Albania"),
            ("+213", "Algeria"),
            ("+54", "Argentina"),
            ("+43", "Austria"),
            ("+32", "Belgium"),
            ("+55", "Brazil"),
            ("+359", "Bulgaria"),
            ("+56", "Chile"),
            ("+86", "China"),
            ("+57", "Colombia"),
            ("+506", "Costa Rica"),
            ("+385", "Croatia"),
            ("+53", "Cuba"),
            ("+357", "Cyprus"),
            ("+420", "Czech Republic"),
            ("+45", "Denmark"),
            ("+20", "Egypt"),
            ("+358", "Finland"),
            ("+33", "France"),
            ("+49", "Germany"),
            ("+30", "Greece"),
            ("+852", "Hong Kong"),
            ("+36", "Hungary"),
            ("+91", "India"),
            ("+62", "Indonesia"),
            ("+353", "Ireland"),
            ("+972", "Israel"),
            ("+39", "Italy"),
            ("+81", "Japan"),
            ("+254", "Kenya"),
            ("+60", "Malaysia"),
            ("+52", "Mexico"),
            ("+31", "Netherlands"),
            ("+234", "Nigeria"),
            ("+47", "Norway"),
            ("+92", "Pakistan"),
            ("+63", "Philippines"),
            ("+48", "Poland"),
            ("+351", "Portugal"),
            ("+40", "Romania"),
            ("+65", "Singapore"),
            ("+27", "South Africa"),
            ("+34", "Spain"),
            ("+46", "Sweden"),
            ("+41", "Switzerland"),
            ("+66", "Thailand"),
            ("+90", "Turkey"),
            ("+380", "Ukraine"),
            ("+971", "United Arab Emirates"),
            ("+84", "Vietnam")
    ]

    phone_country=forms.ChoiceField(
        label="Country",
        required=True,
        choices=phone_country_choices
    )

    phone_number=forms.CharField(
        label="Number",
        max_length=20,
        required=True
    )

    profession_choices = [
        ("psychologist", "Psychologist"),
        ("psychiatrist", "Psychiatrist"), 
        ("clinical social worker", "Clinical Social Worker"), 
        ("other", "Other")
    ]

    profession = forms.ChoiceField(
        label="Profession", 
        choices=profession_choices, 
        required=True
    )

    profession_other = forms.CharField(
        label="If you chose 'Other', please add your answer here",
        max_length=250, 
        required=False
    )

    practice_years_choices = [
        ("<1", "Less than 1 year"), 
        ("1-5", "1-5 years"), 
        ("5-10", "5-10 years"), 
        ("11-15", "11-15 years"), 
        (">15", "More than 15 years")
    ]

    practice_years = forms.ChoiceField(
        label="How many years have you been practicing?", 
        choices=practice_years_choices, 
        required=True
    )

    emdr_choices = [
        ("Basic", "EMDR Basic Training"), 
        ("Advanced", "Advanced Training in Recent Event Protocols"),
        ("R-TEP/G-TEP", "Trained in R-TEP and G-TEP"),
        ("STEP", "Trained in STEP"),
        ("other", "Other")
    ]

    emdr = forms.ChoiceField(
        label="Level of EMDR Training", 
        choices=emdr_choices, 
        help_text="Please describe your current level of EMDR training", 
        required=True
    )

    emdr_other = forms.CharField(
        label="If you chose 'Other', please add your answer here",
        max_length=250,
        required=False
    )

    practice_options = [
        ("individual", "Individual Private Practice"), 
        ("group (less than 10)", "Group Private Practice (less than 10)"), 
        ("group (more than 10)", "Group Private Practice (more than 10)"), 
        ("hospital", "Hospital Setting"),
        ("school", "School Setting"), 
        ("community centre", "Community Mental Health Centre"),
        ("schools k-12", "Schools (K-12)"), 
        ("college", "College/University"),
        ("first responder/military", "First Responder/Military Setting"),
        ("non-profit", "Non-Profit"), 
        ("other", "Other")
    ]

    practice_setting = forms.MultipleChoiceField(
        label="Practice Setting",
        choices=practice_options, 
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    practice_other = forms.CharField(
        label="If you chose 'Other', please describe here", 
        required=False, 
        widget=forms.Textarea
    )

    access_type_choices = [
        ("individual", "Individual Clinician Access"),
        ("organizational", "Organizational Access")
    ]

    access_type = forms.ChoiceField(
        label="Are you interested in individual or organizational access to STEP?", 
        choices=access_type_choices,  
        required=True
    )

    client_population_options = [
        ("children", "Children"),
        ("adolescents", "Adolescents"),
        ("adults", "Adults"), 
        ("older adults", "Older Adults"), 
        ("couples", "Couples"), 
        ("families", "Families"), 
        ("2slgbtqia+", "2SLGBTQIA+"), 
        ("indigenous", "Indigenous"),
        ("first responders/military", "First Responders/Military"),
        ("other", "Other")
    ]

    client_population = forms.MultipleChoiceField(
        label="Client Population Focus",
        choices=client_population_options, 
        widget=forms.CheckboxSelectMultiple,
        help_text="Please select all that apply",
        required=True
    )

    client_population_other = forms.CharField(
        label="If you selected 'Other', please add your answer here",
        widget=forms.Textarea, 
        required=False
    )

    country = forms.CharField(
        label="What country are you from?",
        max_length=200,
        required=True
    )

    message = forms.CharField(
        label="Message",
        widget=forms.Textarea,
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()

        other_error = "This field is required when selecting 'Other'."
        
        profession = cleaned_data.get('profession')
        profession_other = cleaned_data.get('profession_other')
        if profession == 'other' and not profession_other:
            self.add_error(
                "profession_other", 
                other_error
            )

        emdr = cleaned_data.get("emdr")
        emdr_other = cleaned_data.get("emdr_other")
        if emdr == 'other' and not emdr_other:
            print("FOUND EMDR ERROR!")
            self.add_error(
                'emdr_other', 
                other_error
            )

        practice_setting = cleaned_data.get("practice_setting")
        practice_other = cleaned_data.get("practice_other")

        if practice_setting and ('other' in practice_setting) and not practice_other:
            self.add_error(
                "practice_other", 
                other_error
            )

        population = cleaned_data.get("client_population")
        population_other = cleaned_data.get("client_population_other")

        if population and ('other' in population) and not population_other: 
            self.add_error(
                'client_population_other', 
                other_error
            )


        return cleaned_data

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.required:
                field.label_suffix = ' <span class="required-label">(required)</span>'
            else:
                field.label_suffix = ""
