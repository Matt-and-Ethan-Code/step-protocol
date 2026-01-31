from django import forms

class ProviderIntakeForm(forms.Form):
    first_name = forms.CharField(
        label="First name",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Jane",
                "autocomplete": "given-name"
            }
        ), 
        help_text="Enter your first name."
    )

    last_name = forms.CharField(
        label="Last name",
        max_length=50,
        widget=forms.TextInput(attrs={
            "placeholder": "Doe",
            "autocomplete": "family-name"
        }),
        help_text="Enter your last name."
    )

    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={
            "placeholder": "jane.doe@example.com",
            "autocomplete": "email"
        }), 
        help_text="We'll only use this to contact you about your application."
    )

    phone_country=forms.CharField(
        label="Country code",
        max_length=4,
        widget=forms.TextInput(attrs={
            "placeholder": "+1", 
            "autocomplete": "tel-country-code"
        }), 
        help_text="Your country code."
    )

    phone_number=forms.CharField(
        label="Phone number",
        max_length=20,
        widget=forms.TextInput(attrs={
            "placeholder": "555 123 4567",
            "autocomplete": "tel-national"
        }), 
        help_text="Enter the rest of your phone number."
    )