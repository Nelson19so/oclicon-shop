from django import forms
from .models import FrequentlyAskedQuestions, NewsLetterSubscriber

# frequently asked questions form
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

class NewsLetterSubscriberForm(forms.ModelForm):
    class Meta:
        model = NewsLetterSubscriber
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if not email:
            return forms.ValidationError('email field is required')

        if NewsLetterSubscriber.objects.filter(email=email).exists():
            raise forms.ValidationError('email already subscribed')
        return cleaned_data
        