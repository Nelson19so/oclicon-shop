from django import forms
from .models import AdditionalUserInfo, ProfilePicture, BillingAddress
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

# user registration form
User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label="Password",
    error_messages={
        'required': 'Password field is required' 
    })
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", 
    error_messages={
        'required': 'Confirm password field is required'
    })
    username = forms.CharField(max_length=100, required=True, error_messages={
        'required': 'Username field is required'
    })
    email = forms.EmailField(max_length=100, required=True, error_messages={
        'required': 'Email field is required'
    })

    class Meta:
        model = User
        fields = ['username', 'email', 'terms_accepted', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if len(username) <= 3:
            raise forms.ValidationError('Username field is too short*')
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists*")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# user login form
class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'login-email'}),
    required=True, error_messages={
        'required': 'Email field is required'
    })
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login-password'}),
    required=True, error_messages={
        'required': 'Password field is required'
    })

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

# reset password user email
class ResetPasswordEmailForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True, error_messages={
        'required': 'Email field is required'
    })

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if email and not User.objects.filter(email=email).exists():
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
        return cleaned_data

# user profile
class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email',)
        labels = {
            'username': 'username'
        }
        widget = {
            'username': forms.TextInput(attrs={'class': 'profile-input'}),
            'email': forms.EmailInput(attrs={'class': 'profile-input'}),
        }

# additional information
class UserAdditionalInformationForm(forms.ModelForm):
    
    class Meta:
        model = AdditionalUserInfo
        fields = ('related_username', 'second_email', 'phone_number', 'city', 'zip_code', 'country_region')
        widget = {
            'related_username': forms.TextInput(attrs={
                'class': 'profile-input', 'placeholder': 'Enter your related username'
            }),
            'second_email': forms.EmailInput(attrs={
                'class': 'profile-input', 'placeholder': 'Enter second email'
            }),
            'phone_number': forms.TextInput(attrs={
                'type': 'tel', 'class': 'profile-input', 'placeholder': 'Enter your pone number'
            }),
            'city': forms.TextInput(attrs={'class': 'profile-input'}),
            'zip_code': forms.TextInput(attrs={'class': 'profile-input', 'type': 'number',}),
            'country_region': forms.TextInput(attrs={'class': 'profile-input'})
        }

# user profile/avatar form
class UserProfileForm(forms.ModelForm):

    class Meta:
        model = ProfilePicture
        fields = ['profile']
        widget = {
            'profile': forms.FileInput(attrs={'class': 'user_profile_input'})
        }

# bulling form
class BillingAddressForm(forms.ModelForm):

    class Meta:
        model = BillingAddress
        fields = '__all__'
        exclude = ['user']

# change user password while in profile with current and new password
class UserPasswordChange(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'current_password'}),
        required=True
    )

    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'new_password', 'placeholder': '8+ characters'}),
        required=True,
        validators=[validate_password]
    )

    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'confirm_new_password', 'name': 'password'}),
        required=True,
        validators=[validate_password]
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')

        if not self.user.check_password(current_password):
            raise forms.ValidationError('Current password is incorrect')
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('new password and confirm password do not match')
        return cleaned_data
