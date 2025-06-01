from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.core.mail import send_mail
from apps.orders.models import Order, ShippingAddress
from apps.orders.forms import ShippingAddressForm
from .models import (
    CustomUser, SearchHistory, 
    AdditionalUserInfo, ProfilePicture, 
    BillingAddress
)
from .forms import (
    UserRegistrationForm, UserLoginForm, 
    ResetPasswordEmailForm, PasswordResetForm,
    UserProfileForm, UserAdditionalInformation,
    UserForm, BillingAddressForm, 
    UserPasswordChange
)

User = get_user_model()

# registration view set
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
            request.session['name'] = user.Name

            return redirect('welcome_registration', user.id)
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

            if user is not None:
                login(request, user)
                return redirect('dashboard')  # or any page after login

    breadcrumbs = [
        ('User Account', '/home/user_account'),
        ('Sign In', request.path)
    ]

    return render(request, 'accounts/authentication/login.html', {'form': form, 'breadcrumbs': breadcrumbs})

# logout view set
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    request.session['logged-out'] = True
    return redirect("successful_logout")

# successfully logged out
def user_successfully_logged_out(request):
    if request.session.get('logged-out'):
        if not request.user.is_authenticated:
            request.session.pop('logged-out', None) 
            return render(request, 'accounts/logout-successfully.html')
        return redirect('/404')
    else:
        return redirect('home')

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
    return render(request, 'accounts/authentication/password_reset_request.html', context)

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

# user account dashboard
@login_required(login_url='login')
def account_dashboard(request):
    user = request.user
    
    # dashboard breadcrumbs
    breadcrumbs = [
        ('User Account', '#/'),
        ('Dashboard', reverse('dashboard'))
    ]

    # total order filtering for user
    orders = Order.objects.filter(user=user)
    total_orders = orders.count()
    total_pending_order = orders.filter(status='PENDING').count()
    completed_order = orders.filter(status='DELIVERED').count()

    # recent searched
    search_product = SearchHistory.objects.filter(user=user).order_by('-searched_at')[:4]

    # latest 7 orders
    latest_orders = Order.objects.filter(user=user).order_by('-created_at')[:7]

    # additional information
    user_info = AdditionalUserInfo.objects.filter(user=user)

    # billing information
    billing_info = BillingAddress.objects.filter(user=user)
    
    # context processor
    context = {
        'breadcrumbs': breadcrumbs,
        'user': user,
        'orders': orders,
        'total_orders': total_orders,
        'total_pending_order': total_pending_order,
        'completed_order': completed_order,
        'search_product': search_product,
        'latest_orders': latest_orders,
        'user_info': user_info,
        'billing_info': billing_info,
    }
    return render(request, 'accounts/dashboard.html', context)

# order history page
@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user)

    breadcrumbs = [
        ('User Account', '#/'),
        ('Dashboard', reverse('dashboard')),
        ('Order History', reverse('order-history'))
    ]

    context = {'breadcrumbs': breadcrumbs, 'orders': orders}

    return render(request, 'accounts/order-history.html', context)

# user card and address
@login_required(login_url='login')
def card_address(request):

    breadcrumbs = [
        ('User Account', '#/'),
        ('Dashboard', reverse('dashboard')),
        ('Cards & Address', reverse('card-address'))
    ]

    context = {'breadcrumbs': breadcrumbs}
    
    return render(request, 'accounts/card_address.html', context)

# user search history
@login_required(login_url='login')
def search_history(request):

    searched_products = (
        SearchHistory.objects.filter(user=request.user)
        .order_by('-searched_at')
    )

    breadcrumbs = [
        ('User Account', '#/'),
        ('Dashboard', reverse('dashboard')),
        ('Search History', reverse('search-history'))
    ]

    context = {'breadcrumbs': breadcrumbs, 'searched_products': searched_products,}
    
    return render(request, 'accounts/search_history.html', context)


# user settings profile
@login_required(login_url='login')
def user_settings_profile(request):
    user = request.user

    try:
        additional_info = user.additional_user
    except AdditionalUserInfo.DoesNotExist:
        additional_info = None

    try:
        profile = user.profile
    except ProfilePicture.DoesNotExist:
        profile = None

    try:
        billing = user.billing_info
    except BillingAddress.DoesNotExist:
        billing = None

    try:
        shipping = user.shipping_info
    except ShippingAddress.DoesNotExist:
        shipping = None

    user_form = UserForm(instance=user)
    additional_info_form = UserAdditionalInformation(instance=additional_info)
    profile_form = UserProfileForm(instance=profile)
    billing_information = BillingAddressForm(instance=billing)
    shipping_information = ShippingAddressForm(instance=shipping)
    reset_user_password = UserPasswordChange()

    if request.method == 'POST' and 'submit_user_info' in request.POST:
        user_form = UserForm(request.POST, instance=user)
        additional_info_form = UserAdditionalInformation(request.POST, instance=additional_info)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        # form validation
        if user_form.is_valid() and additional_info_form.is_valid() and profile_form.is_valid():
            user_form.save()

            # additional info
            additional_info = additional_info_form.save(commit=False)
            additional_info.user = user
            additional_info_form.save()

            # profile
            profile_instance = profile_form.save(commit=False)
            profile_instance.user = user
            profile_form.save()
            return redirect('profile')

    if request.method == 'POST' and 'submit_billing_info' in request.POST:
        billing_information_form = BillingAddressForm(request.POST, instance=billing)

        if billing_information_form.is_valid():
            billing_instance = billing_information_form.save(commit=False)
            billing_instance.user = user
            billing_instance.save()
            return redirect('profile')
    
    if request.method == 'POST' and 'submit_shipping_info' in request.POST:
        shipping_information_form = ShippingAddressForm(request.POST, instance=shipping)

        if shipping_information_form.is_valid():
            shipping_instance = shipping_information_form.save(commit=False)
            shipping_instance.user = user
            shipping_information_form.save()
            return redirect('profile')

    if additional_info and additional_info.is_complete():
        pass
    else:
        messages.error(request, 'Your account profile is incomplete!')

    breadcrumbs = [
        ('User Account', '#/'),
        ('Dashboard', reverse('dashboard')),
        ('Search History', reverse('search-history'))
    ]

    context = {
        'user_form': user_form,
        'breadcrumbs': breadcrumbs,
        'additional_info_form': additional_info_form,
        'profile_form': profile_form,
        'billing_information': billing_information,
        'shipping_information': shipping_information,
        'reset_user_password' : reset_user_password,
    }

    return render(request, 'accounts/profile.html', context)

# change user password via settings profile
def reset_user_password(request):
    if request.method == 'POST':
        reset_user_password_form = UserPasswordChange(request.user, request.POST)

        if reset_user_password_form.is_valid():
            new_password = reset_user_password_form.cleaned_data['new_password']
            request.user.set_password(new_password)
            request.user.save()

            update_session_auth_hash(request, request.user)
            return redirect('profile')

    return redirect('home')

