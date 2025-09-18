from django.shortcuts    import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.urls         import reverse
from django.contrib.auth.decorators import login_required
from django.utils.http   import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.core.mail    import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from apps.accounts.forms  import (
    UserRegistrationForm, UserLoginForm, 
    ResetPasswordEmailForm, PasswordResetForm,
    UserPasswordChange
)

User = get_user_model()

# User registration view create
def user_registration_view_create(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        # checks if user form is valid
        if form.is_valid():
            # saves the user form to the db
            user = form.save()
            # chooses the user auth method for saving user details
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            # Store session data temporarily
            request.session['confirm_session'] = True
            request.session['user_id'] = user.id
            request.session['name'] = user.username

            return redirect('welcome_user', user.id)
    else:
        form = UserRegistrationForm()

    breadcrumbs = [
        ('User Account', '#/'),
        ('Sign Up', request.path)
    ]

    context = {"form": form, "breadcrumbs": breadcrumbs}

    return render(request, 'accounts/authentication/register.html', context)

# welcome registration session 
def welcome_registration_view(request, user_id):
    # checks if user has a registration session and user is authenticated
    if request.session.get('confirm_session') and request.user.is_authenticated:

        # Ensure user_id matches the session for security
        if request.user.id != user_id:
            
            return redirect('home')

        # getting the user name and email for use in  the template
        user_name = request.session.get('name')
        user_email = request.user.email

        # Clear session to prevent revisits this page again
        request.session.pop('confirm_session', None)
        request.session.pop('user_id', None)
        request.session.pop('name', None)

        return render(request, 'accounts/welcome_registration.html', {
            "name":          user_name,
            "email":         user_email,
        })

    return redirect('home')

# user log in view create
def login_view(request):
    # user log in form for posting user details
    form = UserLoginForm(request.POST or None)

    # checks if user is authenticated, if true then returns the user to home
    if request.user.is_authenticated:
        return redirect('home')

    # handling post request for logging in users in
    if request.method == 'POST':

        # checks if form is valid
        if form.is_valid():
            
            # getting user email and password since the user fields are valid
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            # authenticating validated user email and password
            user = authenticate(request, email=email, password=password)

            # Checks if the user authenticated is found or None
            if user is not None:
                # if user is exist in our db
                login(request, user)
                return redirect('dashboard')  # or any page after login

    # creates breadcrumb for login page
    breadcrumbs = [
        ('User Account', '/home/user_account'),
        ('Sign In', request.path)
    ]

    # renders template for login page
    return render(request, 'accounts/authentication/login.html', {
        'form': form, 
        'breadcrumbs': breadcrumbs
    })

# logout view set
@login_required(login_url='login')
def logout_view(request):
    # getting the user name of the user logging out
    request.session['logged-out-username'] = request.user.username

    # logs out user
    logout(request)

    # set logged out user to true
    request.session['logged-out'] = True

    return redirect("successful_logout")

# successfully logged out
def user_successfully_logged_out(request):
    # checks if there's session for logged out user
    if request.session.get('logged-out'):

        # checks if user is authenticated
        if not request.user.is_authenticated:
            # getting logged out user name session
            username = request.session.pop('logged-out-username', 'user')
            
            # deleting the user logged out session
            request.session.pop('logged-out', None)
            
            # rendering template for logged out user
            return render(request, 'accounts/logout-successfully.html', {
                'name': username
            })

        # if user is authenticated/logged in
        return redirect('/404')
    
    # if no session exist for logged out user
    else:
        return redirect('home')

# View for requesting password reset (Step 1)
def reset_password_request_view(request):
    # handles post request for forgotten password
    if request.method == 'POST':
        form = ResetPasswordEmailForm(request.POST)
        
        # checks if form is valid
        if form.is_valid():
            # getting user field email from the db
            email = form.cleaned_data['email']

            try:

                # getting user with this email
                user = User.objects.get(email=email)
            
            except User.DoesNotExist:
                return redirect('reset_password_request')
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
    
            reset_url = request.build_absolute_uri(f'/reset/{uid}/{token}/')
            
            # render email html
            html_content = render_to_string('email/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
    
            try:

                # send the password reset link to the user's email
                send__message = EmailMultiAlternatives(
                    subject='Password Reset Request',
                    body=html_content,
                    from_email='no-reply@clickon.com',
                    to=[email]
                )
                send__message.attach_alternative(html_content, "text/html")
                send__message.send()
        
            except Exception as e:
                return redirect('reset_password_request')  

            # Redirect to a page saying email has been sent
            return redirect('password_reset_email_sent')  

    else:
        form = ResetPasswordEmailForm()

    # creates breadcrumbs for the forgot password page
    breadcrumbs = [
        ('User Account', '/home/user_account'),
        ('Sign In', reverse('login')),
        ('Forgot Password', request.path)
    ]
    context = {'form': form, 'breadcrumbs': breadcrumbs}
    return render(request, 'accounts/authentication/password_reset_request.html', context)


# View for resetting the password (Step 2)
def reset_password_view(request, uidb64, token):
    # validating if the uidb64 exist for the user
    try:
        # Decode the user ID
        uid = urlsafe_base64_decode(uidb64).decode() 
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # checks if token exist for this user
    if user and default_token_generator.check_token(user, token):
        # handles post request for user
        if request.method == 'POST':
            # passes password form
            form = PasswordResetForm(request.POST)

            # checks if password form is valid
            if form.is_valid():
                # Save the new password
                user.set_password(form.cleaned_data['password1'])
                user.save()

                # Redirect to a success page
                return redirect('password_reset_success') 
        else:
            form = PasswordResetForm()

        # creates breadcrumb for this page
        breadcrumbs = [
            ('User Account', '/home/user_account'),
            ('Sign In', reverse('login')),
            ('Forget Password', reverse('reset_password_request')),
            ('Reset Password', request.path)
        ]
        context = {'form': form, 'breadcrumbs': breadcrumbs}
        return render(request, 'accounts/authentication/password_reset_page.html', context)
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
    return render(request, 'accounts/authentication/email_verify_code.html', context)


# change user password via settings profile
def reset_user_password(request):
    # handles post request
    if request.method == 'POST':
        # reset_password_form
        reset_user_password_form = UserPasswordChange(request.user, request.POST)

        # checks if form is valid or not
        if reset_user_password_form.is_valid():
            # getting new password since the form is valid
            new_password = reset_user_password_form.cleaned_data['new_password']
            # setting the new password to te new user
            request.user.set_password(new_password)
            # saving the form
            request.user.save()

            update_session_auth_hash(request, request.user)
            return redirect('profile')
        else:
            reset_user_password_form = UserPasswordChange(request.user)            

    return redirect('profile')
