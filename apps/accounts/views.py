from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm, ResetPasswordEmailForm, PasswordResetForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

# Create your views here.

User = get_user_model()

# registration view set
def user_registration_view_create(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Store session data temporarily
            request.session['confirm_session'] = True
            request.session['user_id'] = user.id
            request.session['name'] = user.name

            return redirect('welcome_registration', user.id)
    else:
        form = UserRegistrationForm()

    breadcrumbs = [
        ('User Account', '/home/user_account'),
        ('Sign Up', request.path)
    ]

    return render(request, 'accounts/authentication/Register.html', {"form": form, "breadcrumbs": breadcrumbs})

# welcome registration session 
def welcome_registration_view(request, user_id):
    if request.session.get('confirm_session') and request.user.is_authenticated:
        # Ensure user_id matches the session for security
        if request.user.id != user_id:
            return redirect('home')

        user_name = request.session.get('name')
        user_email = request.user.email  # authenticated user

        # Clear session to prevent revisits
        request.session.pop('confirm_session', None)
        request.session.pop('user_id', None)
        request.session.pop('name', None)

        return render(request, 'accounts/welcome_registration.html', {
            "name": user_name,
            "email": user_email,
        })

    return redirect('home')

# log in view create
def login_view(request):
    form = UserLoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')  # or any page after login

    breadcrumbs = [
        ('User Account', '/home/user_account'),
        ('Sign In', request.path)
    ]

    return render(request, 'accounts/authentication/Login.html', {'form': form, 'breadcrumbs': breadcrumbs})

# logout view set 
def logout_view(request):
    logout(request)
    messages.info(request, 'logged out successfully')
    return redirect("home")

# user profile view update
@login_required(login_url='login')
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # redirect to a profile page or dashboard
    else:
        form = UserProfileUpdateForm(instance=user)
    
    return render(request, 'account/update_profile.html', {'form': form})

# View for requesting password reset (Step 1)
def reset_password_request_view(request):
    if request.method == 'POST':
        form = ResetPasswordEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)  # Generate a reset token
            uid = urlsafe_base64_encode(str(user.pk).encode()).decode()  # Encode the user ID
            # Send the password reset link to the user's email
            send_mail(
                'Password Reset Request',
                f'Click this link to reset your password: /reset/{uid}/{token}/',
                'no-reply@clicon.com',
                [email],
            )
            return redirect('password_reset_email_sent')  # Redirect to a page saying email has been sent
    else:
        form = ResetPasswordEmailForm()
    breadcrumbs = [
        ('User Account', '/home/user_account'),
        ('Sign In', reverse('login')),
        ('Forget Password', request.path)
    ]
    context = {'form': form, 'breadcrumbs': breadcrumbs}
    return render(request, 'accounts/authentication/Password_reset_request.html', context)

# View for resetting the password (Step 2)
def reset_password_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode the user ID
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                # Save the new password
                user.set_password(form.cleaned_data['password1'])
                user.save()
                return redirect('password_reset_success')  # Redirect to a success page
        else:
            form = PasswordResetForm()

        breadcrumbs = [
            ('User Account', '/home/user_account'),
            ('Sign In', reverse('login')),
            ('Forget Password', reverse('reset_password_request')),
            ('Reset Password', request.path)
        ]
        context = {'form': form, 'breadcrumbs': breadcrumbs}
        return render(request, 'accounts/authentication/Password_reset_page.html', context)
    else:
        return redirect('password_reset_invalid')  # Redirect if token is invalid or expired

# email verification code for user registration confirmation
def registration_email_verification(request):
    breadcrumbs = [
        ('User Account', '/home/user_account'),
        ('Sign Up', reverse('register')),
        ('Email Verification', request.path)
    ]

    context = {'breadcrumbs': breadcrumbs}
    return render(request, 'accounts/authentication/Email_verify_code.html', context)

# user account dashboard
def account_dashboard(request):
    breadcrumbs = [
        ('User Account', '#/'),
        ('Dashboard', reverse('dashboard'))
    ]
    context = {'breadcrumbs': breadcrumbs}
    return render(request, 'accounts/dashboard.html', context)
