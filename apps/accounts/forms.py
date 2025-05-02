from django.forms import Form
from django import forms
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

# user registration form
class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'terms_accepted', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exist")
        return email


# user login form
class UserLoginFrom(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.clean_data.get("email")
        password = self.clean_data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise forms.ValidationError("Invalid credentials")
        return self.cleaned_data


# profile update form
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'terms_accepted']