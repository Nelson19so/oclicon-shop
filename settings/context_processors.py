# apps/product/context-processor

from apps.products.models import Category, Product, Ad
from apps.cart.models import CartItem, Cart
from django.contrib.sessions.models import Session

# context processor for category list for navbar
def navbar_categories_list(request):
    # filters all category and it related children
    categories = Category.objects.prefetch_related('children').filter(parent=None)
    # returns the category for use.
    return {"categories": categories}

# ads
def active_ads(request):
    return {
        'top_ads': Ad.objects.filter(position='top', is_active=True),
        'bottom_ads': Ad.objects.filter(position='bottom', is_active=True),
        'sidebar_ads': Ad.objects.filter(position='sidebar', is_active=True),
        'popup_ads': Ad.objects.filter(position='popup', is_active=True),
    }

# featured product filtering for home
# def featured_product(request):
#     pass

# # filtering computer accessories for home
# def computer_accessories(request):
#     pass

# navbar cart view
def navbar_cart_display_list(request):
    # requesting for authenticated user
    user = request.user

    try:
        # checks if user is authenticated
        if user.is_authenticated:
            # filters cart item for authenticated user
            cart = Cart.objects.get(user=user)

            # then filters cart item for user cart
            cart_items = CartItem.objects.filter(cart=cart)[:3]
        
        else:
            # if theres no session for anonymous user
            if not request.session.session_key:
                # creating new session for anonymous user
                request.session.create()
    
            # requesting for anonymous user session
            session_key = request.session.session_key
            
            # getting session for anonymous user
            session = Session.objects.get(session_key=session_key)
            # tries to get data for anonymous user session
            cart = Cart.objects.get(session_id=session)
            # getting cart item for the session cart
            cart_items = CartItem.objects.filter(cart=cart)[:3]

    # if cart does not exist
    except (Cart.DoesNotExist or Session.DoesNotExist):
        # returns empty tuple to avoid conflict
        cart_items = []

    # returns the cart item for use.
    return {'cart_items': cart_items}

# breadcrumbs 
# not yet in settings.py context processor
def breadcrumbs_processor(request):
    return {
        'breadcrumbs': []  # default fallback
    }
