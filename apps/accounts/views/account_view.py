from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from apps.orders.models import Order, ShippingAddress
from apps.orders.forms import ShippingAddressForm
from apps.products.models import SearchHistory
from apps.accounts.models import (
    AdditionalUserInfo, 
    ProfilePicture, BillingAddress
)
from apps.accounts.forms import (
    UserProfileForm, UserAdditionalInformation,
    UserForm, BillingAddressForm, 
    UserPasswordChange
)

User = get_user_model()

# user account dashboard
@login_required(login_url='login')
def account_dashboard(request):
    user = request.user
    
    # dashboard breadcrumbs
    breadcrumbs = [
        ('User Account', '#/'),
        ('Dashboard', reverse('dashboard'))
    ]

    try:
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
    except (
        Order.DoesNotExist or AdditionalUserInfo.DoesNotExist or 
        BillingAddress.DoesNotExist, SearchHistory.DoesNotExist
    ):
        pass
    
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
    try:
        orders = Order.objects.filter(user=request.user)
    except Order.DoesNotExist:
        pass

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
    try:
        searched_products = (
            SearchHistory.objects.filter(user=request.user)
            .order_by('-searched_at')
        )
    except SearchHistory.DoesNotExist:
        pass

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
        pass # passes this condition if all fields are filled up
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

# Delete user account function
def delete_user_account(request):
    user = request.user
    user.delete()
    return redirect('home')
