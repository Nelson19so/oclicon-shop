from django.shortcuts     import render, get_object_or_404
from apps.products.models import Product
from apps.cart.models     import Cart, CartItem, WishlistProduct
from django.http          import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.generic import View

class SessionMixin:

    def get_or_create_session_key(self, request):
        if not request.session.session_key:
            request.session.create()

        return request.session.session_key

# product wishlist view create
class WishListProductCreate(View):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = kwargs.get('product_id')

        # filters product or 404 if not found
        product = get_object_or_404(Product, id=product_id)

        # checks if user is authenticated
        if user.is_authenticated:
           
            if not WishlistProduct.objects.filter(user=user, product=product).exists():
                WishlistProduct.objects.create(user=user, product=product)
    
        else:
            session_key = request.session.session_key

            if not session_key:
                request.session.create()

            session_key = request.session.session_key
        
            if not session_key:
                return JsonResponse({
                    'status':  'error',
                    'message': 'No session found',
                }, status=201)

            # checks for existing item 
            if not WishlistProduct.objects.filter(session_key=session_key, product=product).exists():
                WishlistProduct.objects.create(session_key=session_key, product=product)
           
        return JsonResponse({
            'status':  'success',
            'message': 'Added item to wishlist',
        }, status=201)

# removes items from wishlist
class RemoveItemFromWishlist(View):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        # getting the product id
        product = get_object_or_404(Product, id=kwargs.get('product_id'))
        mixin = SessionMixin()
        
        # requesting for the authenticated user 
        user = request.user

        # checks if user is authenticated
        if user.is_authenticated:
            # filters wishlist product for the user and also the product with the id and delete
            WishlistProduct.objects.filter(user=user, product=product).delete()

        # if not authenticated user, then anonymous users
        else:
            # filters session id for anonymous user session
            session_key = mixin.get_or_create_session_key(request)

            # deleting session for anonymous user
            WishlistProduct.objects.filter(session_key=session_key, product=product).delete()

        # returns Json message if success
        return JsonResponse({
            'status':  'success',
            'message': 'Product removed from wishlist'
        })

# wishlist page view
def wish_list_view(request):
    # request for authenticated user
    user = request.user
    wishlists = []
    mixin = SessionMixin()
    session_key = mixin.get_or_create_session_key(request)
    
    try:

        # if user is authenticated
        if user.is_authenticated:
            # filters wishlist product for user
            wishlists = WishlistProduct.objects.filter(
                user=user
            ).select_related('product')

        # else if not authenticated and no session id for anonymous user 
        else:
            # filtering wishlist for anonymous user
            wishlists = WishlistProduct.objects.filter(session_key=session_key)

        # if user is authenticated
        if user.is_authenticated:
            cart = Cart.objects.get(user=user) 

        # anonymous users
        else:
            cart = Cart.objects.get(session_key=session_key) 

        for wishlist in wishlists:
            wishlist.in_cart = False

        # cart item filter
        if cart and CartItem.objects.filter(
            cart=cart,
            product=wishlist.product
        ).exists():
            wishlist.in_cart = True

    except (Cart.DoesNotExist or CartItem.DoesNotExist or WishlistProduct.DoesNotExist):
        pass
    
    # builds breadcrumbs for user
    breadcrumbs = [
        ('Wishlist', request.path)
    ]
    
    # renders context processor for use in the UI
    context = {
        "wishlists":   wishlists,
        "user":        user, 
        'breadcrumbs': breadcrumbs,
    }

    return render(request, 'cart/wishlist.html', context)
