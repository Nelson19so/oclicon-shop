from django.forms import Form
from django import forms
from .models import Comments, NewsLetterSubscriber

# user comment form
class UserCommentsForm(forms.ModelForm):
    
    class Meta:
        model = Comments
        fields = ('parent', 'full_name', 'email', 'message')

# user news letter form
class NewsLetterSubscriberForm(forms.ModelForm):

    class Meta:
        model = NewsLetterSubscriber
        fields = ['email']