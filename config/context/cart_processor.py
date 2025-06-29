from apps.cart.models import CartItem, Cart

# navbar cart view
def cart_list(request):
    # requesting for authenticated user
    user = request.user
    cart = None
    total_cart_price = 0
    cart_items = []
    nav_cart_count = 0

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
    
    if len(cart_items) > 0:
        nav_cart_count = cart_items.count()

    # returns the cart item for use.
    return {
        'cart_items': cart_items[:2], 
        'total_cart_price': total_cart_price, 
        'nav_cart_count': nav_cart_count
    }
