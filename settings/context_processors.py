from apps.products.models import Category, Product, Ad, ProductHighlight
from apps.cart.models import CartItem, Cart
from django.contrib.sessions.models import Session

# context processor for category list for navbar
def navbar_categories_list(request):
    # filters all category and it related children
    categories = Category.objects.prefetch_related('children').filter(parent=None)
    # returns the category for use.
    return {"categories": categories}

# product ads
def active_ads(request):
    # getting top ad for home page
    top_ad = Ad.objects.filter(is_active=True, position='top').first()

    if top_ad is None:
        pass
    
    # top right ad
    top_right_ad = Ad.objects.filter(is_active=True, position='top-right-banner').first()

    if top_right_ad is None:
        pass

    # top right bottom ad
    top_right_bottom_ad = Ad.objects.filter(
        is_active=True, position='top-right-two-banner'
    ).first()

    if top_right_bottom_ad is None:
        pass

    featured_ad_highlight = ProductHighlight.objects.filter(features='featured_product').first()

    featured_sidebar_ad = Ad.objects.filter(
        is_active=True,
        position='Sidebar',
        highlight=featured_ad_highlight,
    ).first()

    if featured_sidebar_ad is None:
        pass

    # getting the middle banner ad
    middle_banner_ads = Ad.objects.filter(
        is_active=True,
        position='middle_banner'
    ).order_by('-created_at')[:2]

    if middle_banner_ads is None:
        pass

    # getting the first bottom banner ad
    first_bottom_banner = Ad.objects.filter(
        is_active=True,
        position='bottom'
    ).filter()

    if first_bottom_banner is None:
        pass

    return {
        'top_ad': top_ad,
        'top_right_ad': top_right_ad,
        'top_right_bottom_ad': top_right_bottom_ad,
        'middle_banner_ads': middle_banner_ads,
        'first_bottom_banner': first_bottom_banner,
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
    cart = None
    total_cart_price = 0
    cart_items = []

    # checks if user is authenticated
    try:
        if user.is_authenticated:
            # filters cart item for authenticated user
            cart = Cart.objects.get(user=user)
            total_cart_price = cart.total_price()

            # then filters cart item for user cart
            cart_items = CartItem.objects.filter(cart=cart)[:2]
    
        else:
            # if theres no session for anonymous user
            if not request.session.session_key:
                # creating new session for anonymous user
                request.session.create()
    
            # requesting for anonymous user session
            session_key = request.session.session_key
            # tries to get data for anonymous user session
            cart = Cart.objects.get(session_key=session_key)
            # total cart for anonymous users
            total_cart_price = cart.total_price()
            # getting cart item for the session cart
            cart_items = CartItem.objects.filter(cart=cart)
            
    # if cart does not exist
    except (Cart.DoesNotExist):
        # returns empty tuple to avoid conflict
        cart_items = []
    
    nav_cart_count = cart_items.count()

    # returns the cart item for use.
    return {
        'cart_items': cart_items[:2], 
        'total_cart_price': total_cart_price, 
        'nav_cart_count': nav_cart_count
    }

# breadcrumbs
# not yet in settings.py context processor
def breadcrumbs_processor(request):
    return {
        'breadcrumbs': []  # default fallback
    }
