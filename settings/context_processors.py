from apps.products.models import Category
from apps.cart.models import CartItem, Cart
from django.contrib.sessions.models import Session

# context processor for category list for navbar
def navbar_categories_list(request):
    categories = Category.objects.prefetch_related('children').filter(parent=None)
    return {"categories": categories}

# navbar cart view
def navbar_cart_display_list(request):
    session_id = request.session.session_key
    user = request.user

    if user.is_authenticated:
        cart = Cart.objects.filter(user=user)
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
        else:
            cart_items = []
    
    if not session_id:
        request.session.create()
        request.session.session_key

    try:
        cart = Cart.objects.get(session_id=session_id)
        cart_items = CartItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        cart_items = []

    return {'cart_items': cart_items}

# breadcrumbs 
# not yet in settings.py context processor
def breadcrumbs_processor(request):
    return {
        'breadcrumbs': []  # default fallback
    }
