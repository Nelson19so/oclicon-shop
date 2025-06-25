from django.shortcuts import render, get_object_or_404, redirect
from apps.products.models import Product
from .models import Cart, CartItem, WishlistProduct
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponseNotAllowed
from django.utils import timezone

class SessionMixin:
    def get_or_create_session_key(self, request):
        if not request.session.session_key:
            request.session.create()
        return request.session.session_key

# cart mixin for all cart product
class CartMixin(SessionMixin):
    def cart_item_count(self, request):
        user = request.user

        if user.is_authenticated:
            cart = Cart.objects.get(user=user)
        
        else:
            if not request.session.session_key:
                return 0
            session_key = request.session.session_key
            cart = Cart.objects.filter(session_key=session_key).first()

        return CartItem.objects.filter(cart=cart).count()

    def cart_items_list(self, request):
        user = request.user
        cart = None

        try:
            if user.is_authenticated:
                cart = Cart.objects.get(user=user)
            else:
                session_key = self.get_or_create_session_key(request)
                cart = Cart.objects.get(session_key=session_key)
        except Cart.DoesNotExist:
            return CartItem.objects.none()

        return CartItem.objects.filter(cart=cart)

# create cart item for user and anonymous user
class CreateCartItem(CartMixin, SessionMixin, View):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        # filters product for renders 404 if the id does not exist
        product = get_object_or_404(Product, id=kwargs.get('product_id'))
        user = request.user

        if user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=user)

        else:
            session_key = self.get_or_create_session_key(request)
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

        cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)

        if not created:
            cart_item.quantity = 1
            cart_item.save()

        cart_count = self.cart_item_count(request)
        
        return JsonResponse({
            'status': 'success',
            'count': cart_count
        })

# view form removing items from cart list
class RemoveItemFromCart(View, SessionMixin):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        cart_id = kwargs.get('cart_id')
        user = request.user
        cart_item = []
        cart = None

        if user.is_authenticated:
            cart = Cart.objects.get(user=user)

        else:
            session_key = self.get_or_create_session_key(request)
            cart = Cart.objects.get(session_key=session_key)

        if not cart:
            return JsonResponse({
                'status': 'Cart not found', 
            }, status=404)
            
        cart_item = get_object_or_404(CartItem, cart=cart, id=cart_id)
        cart_item.delete()

        return JsonResponse({
            'status': 'success',
        })

class CartItemListView(CartMixin, ListView, SessionMixin):
    template_name = "cart/cart.html"
    context_object_name = "carts"

    def get_queryset(self):
        return self.cart_items_list(self.request)
    
    def get_breadcrumbs(self):
        breadcrumbs = [
            ('Shopping Cart', self.request.path)
        ]
        return breadcrumbs
    
    # get total price
    def get_total_price(self, request):
        cart = 0

        try:
            if request.user.is_authenticated:
                cart = Cart.objects.get(user=request.user)
                cart = cart.total_price()
            else:
                session_key = self.get_or_create_session_key(request)
                cart = Cart.objects.get(session_key=session_key)
                cart = cart.total_price()
        except Cart.DoesNotExist:
            pass
        return cart
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        context['total_price'] = self.get_total_price(self.request)
        return context

# update cart product quantity view create
@require_POST
def update_cart_quantities(request):
    user = request.user
    cart = None
    session_mixin = SessionMixin()

    try:
        if user.is_authenticated:
            cart = Cart.objects.get(user=user)
        else:
            if not request.session.session_key:
                request.session.create()
        
                session_key = session_mixin.get_or_create_session_key(request)
                cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        return redirect('cart_list')

    item_ids = request.POST.getlist('item_ids')

    if not item_ids:
        return redirect('cart_list')

    # Loop through posted quantities
    for item_id in item_ids:
        quantity = request.POST.get(f'quantity_{item_id}')

        try:
            quantity = int(quantity)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.quantity = quantity
            cart_item.updated_at = timezone.now()
            cart_item.save()
        except (ValueError, CartItem.DoesNotExist):
            # skip invalid entries silently
            return redirect('cart_list')

    return redirect('cart_list')

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
                    'status': 'error',
                    'message': 'No session found',
                }, status=201)

            # checks for existing item 
            if not WishlistProduct.objects.filter(session_key=session_key, product=product).exists():
                WishlistProduct.objects.create(session_key=session_key, product=product)
           
        return JsonResponse({
            'status': 'success',
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
            'status': 'success',
            'message': 'Product removed from wishlist'
        })

# wishlist page view
def wish_list_view(request):
    # request for authenticated user
    user = request.user
    wishlists = []
    mixin = SessionMixin()
    session_key = mixin.get_or_create_session_key(request)
    
    # if user is authenticated
    if user.is_authenticated:
        # filters wishlist product for user
        wishlists = WishlistProduct.objects.filter(user=user).select_related('product')

    # else if not authenticated and no session id for anonymous user 
    else:
        # filtering wishlist for anonymous user
        wishlists = WishlistProduct.objects.filter(session_key=session_key)


    # if user is authenticated
    if user.is_authenticated:
        try:
            cart = Cart.objects.get(user=user) 

            for wishlist in wishlists:
                wishlist.in_cart = False

                if cart and CartItem.objects.filter(
                    cart=cart,
                    product=wishlist.product
                ).exists():
                    wishlist.in_cart = True
        except (Cart.DoesNotExist or CartItem.DoesNotExist):
            pass

    # anonymous users
    else:
        try:
            cart = Cart.objects.get(session_key=session_key) 

            for wishlist in wishlists:
                wishlist.in_cart = False

                if cart and CartItem.objects.filter(
                    cart=cart,
                    product=wishlist.product
                ).exists():
                    wishlist.in_cart = True
        except (Cart.DoesNotExist or CartItem.DoesNotExist):
            pass
    
    # builds breadcrumbs for user
    breadcrumbs = [
        ('Wishlist', request.path)
    ]
    
    # renders context processor for use in the UI
    context = {
        "wishlists": wishlists,
        "user": user, 
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'cart/wishlist.html', context)