from django.forms import Form
from django import forms
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

# user registration form
User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['Name', 'email', 'terms_accepted', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError({"password2": "Passwords do not match."})

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# user login form
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = None  # Store authenticated user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise forms.ValidationError("Invalid email or password")
        
        self.user = user  # Store for later use in view
        return cleaned_data

# profile update form
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'Name', 'terms_accepted']

# reset password user email
class ResetPasswordEmailForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        user = User.objects.filter(email=email)

        if not user:
            raise forms.ValidationError('This email is not register')
        return cleaned_data


# password reset input
class PasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
