from django.forms import Form
from django import forms
from .models import FrequentlyAskedQuestions

# Faqs ---------------
class FrequentlyAskedQuestionsForms(forms.ModelForm):
    class Meta:
        model = FrequentlyAskedQuestions
        fields = ('email', 'subject', 'description')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        subject = cleaned_data.get('subject')
        description = cleaned_data.get('description')

        if not email or not subject or not description:
            raise forms.ValidationError('All fields are required')

        return cleaned_data
