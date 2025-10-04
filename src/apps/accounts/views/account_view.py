from django.shortcuts import render, redirect
from django.contrib   import messages
from django.urls      import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth  import get_user_model
from src.apps.orders.models   import Order, ShippingAddress
from src.apps.orders.forms    import ShippingAddressForm
from src.apps.products.models import ProductSearchHistory
from src.apps.accounts.models import (
    AdditionalUserInfo, 
    ProfilePicture, BillingAddress
)
from src.apps.accounts.forms  import (
    UserProfileForm, UserAdditionalInformationForm,
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
        search_product = ProductSearchHistory.objects.filter(user=user).order_by('-searched_at')[:4]

        # latest 7 orders
        latest_orders = Order.objects.filter(user=user).order_by('-created_at')[:7]

        # additional information
        user_info = AdditionalUserInfo.objects.filter(user=user)

        # billing information
        billing_info = BillingAddress.objects.filter(user=user)
    except (
        Order.DoesNotExist or AdditionalUserInfo.DoesNotExist or
        BillingAddress.DoesNotExist, ProductSearchHistory.DoesNotExist
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
            ProductSearchHistory.objects.filter(user=request.user)
            .order_by('-searched_at')
        )
    except ProductSearchHistory.DoesNotExist:
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

    # Get related instances or None
    additional_info = getattr(user, 'additional_user', None)
    profile = getattr(user, 'profile', None)
    billing = getattr(user, 'billing_info', None)
    shipping = getattr(user, 'shipping_info', None)

    # Initialize forms with existing instances
    user_form = UserForm(instance=user)
    additional_info_form = UserAdditionalInformationForm(instance=additional_info)
    profile_form = UserProfileForm(instance=profile)
    billing_information = BillingAddressForm(instance=billing)
    shipping_information = ShippingAddressForm(instance=shipping)
    reset_user_password = UserPasswordChange()

    # --- Handle User info Submit ---
    if request.method == 'POST' and 'submit_user_info' in request.POST:
        user_form = UserForm(request.POST, instance=user)
        additional_info_form = UserAdditionalInformationForm(request.POST, instance=additional_info)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        # Handle user form validation
        if all([user_form.is_valid(), additional_info_form.is_valid(), profile_form.is_valid()]):
            user_form.save()

            add_info = additional_info_form.save(commit=False)
            add_info.user = user
            add_info.save()

            prof = profile_form.save(commit=False)
            prof.user = user
            prof.save()
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
    
    # remove user profile picture
    if request.method == 'POST' and 'remove_profile' in request.POST:
        try:
            ProfilePicture.objects.filter(user=user).delete()
        except ProfilePicture.DoesNotExist:
            pass

    if additional_info and additional_info.is_complete():
        pass # passes this condition if all fields are filled up
    else:
        messages.error(request, 'Your account profile is incomplete!')

    breadcrumbs = [
        ('User Account', '#/'),
        ('Dashboard', reverse('dashboard')),
        ('Search History', reverse('profile'))
    ]

    context = {
        'user_form': user_form,
        'breadcrumbs': breadcrumbs,
        'additional_user': additional_info_form,
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
