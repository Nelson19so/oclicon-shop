from django.shortcuts import render, get_object_or_404, redirect
from apps.products.models import Product
from .models import Cart, CartItem, WishlistProduct
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, View
from django.contrib.sessions.models import Session
from django.http import HttpResponseNotAllowed
from .forms import *
from django.utils import timezone

# cart mixin for all cart product
class CartMixin:
    def cart_item_count(self, request):
        user = request.user

        if user.is_authenticated:
            cart = Cart.objects.get(user=user)
            return CartItem.objects.filter(cart=cart).count()
        
        if not request.session.session_key:
            return 0
        session = Session.objects.get(session_key=request.session.session_key)
        cart = Cart.objects.filter(session_id=session)
        return CartItem.objects.filter().count()

    def cart_items_list(self, request):
        user = request.user

        try:
            if user.is_authenticated:
                cart = Cart.objects.get(user=user)

            else:
                if not request.session.session_key:
                    request.session.create()
                    
                session_id = request.session.session_key
                session = Session.objects.get(session_key=session_id)

                cart = Cart.objects.get(session=session)
        except (Cart.DoesNotExist or Session.DoesNotExist):
            cart = None

        return CartItem.objects.filter(cart=cart)

# create cart item for user and anonymous user
class CreateCartItem(CartMixin, View):
    @method_decorator([require_POST])
    def post(self, request, *args, **kwargs):
        # filters product for renders 404 if the id does not exist
        product = get_object_or_404(Product, id=kwargs.get('product_id'))
        user = request.user

        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
            cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)

            if not created:
                cart_item.quantity = 1
                cart_item.save()

        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key

            session = Session.objects.get(session_key=session_id)
            cart, created = Cart.objects.get(session=session)
            cart_item, created = CartItem.objects.get(product=product, cart=cart)

            if not created:
                cart_item.quantity = 1
                cart_item.save()

        cart_count = self.cart_item_count(request)
        
        return JsonResponse({
            'status': 'success',
            'count': cart_count
        })

# view form removing items from cart list
class RemoveItemFromCart(View):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        cart_id = kwargs.get('cart_id')
        user = request.user
        session_id = request.session.session_key
        cart_item = []
        cart = None

        if user.is_authenticated:
            cart = Cart.objects.get(user=user)

            if cart:
                cart_item = get_object_or_404(CartItem, id=cart_id)

        else:
            if not session_id:
                request.session.create()
            session_id = request.session_key

            session = Session.objects.get(session_key=session_id)
            cart = Cart.objects.get(session=session)

            if cart:
                cart_item = get_object_or_404(CartItem, cart=cart, id=cart_id)

        cart_item.delete()

        return JsonResponse({
            'status': 'success',
        })

class CartItemListView(CartMixin, ListView):
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

        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
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

    if user.is_authenticated:
        cart = Cart.objects.get(user=user)
    else:
        if not session_id:
            request.session.create()
        session_id = request.session.session_key
        session = Session.objects.get(session_key=session_id)
        cart = Cart.objects.filter(session=session)

    if not cart:
        return redirect('cart_list')

    item_ids = request.POST.getlist('item_ids')

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
            continue

    return redirect('cart_list')

# product wishlist view create
class WishListProductCreate(View):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        user = request.user
        session_id = request.session.session_key
        product_id = kwargs.get('product_id')

        # filters product or 404 if not found
        product = get_object_or_404(Product, id=product_id)

        # checks if user is authenticated
        if user.is_authenticated:
            exists = WishlistProduct.objects.filter(user=user, product=product).exists()
            if not exists:
                WishlistProduct.objects.create(user=user, product=product)
        else:
            if not session_id:
                request.session.create()
                session_id = request.session.session_key

            exists = WishlistProduct.objects.filter(session=session_id, product=product).exists()
            if not exists:
                WishlistProduct.objects.create(session=session_id, product=product)

        return JsonResponse({
            'status': 'success',
            'message': 'Added item to wishlist'
        })

# removes items from wishlist
class RemoveItemFromWishlist(View):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        # getting the product id
        product = get_object_or_404(Product, id=kwargs.get('product_id'))
        
        # requesting for the authenticated user 
        user = request.user

        # filters session id for anonymous user session
        session_id = request.session.session_key

        # checks if user is authenticated
        if user.is_authenticated:
            # filters wishlist product for the user and also the product with the id and delete
            WishlistProduct.objects.filter(user=user, product=product).delete()

        # if not authenticated user, then anonymous users
        else:
            # if not session id
            if not session_id:

                # creating new session
                request.session.create()

            # getting anonymous user session
            session = Session.objects.get(session_key=session_id)

            # deleting session for anonymous user
            WishlistProduct.objects.filter(session=session, product=product).delete()

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
    
    # if user is authenticated
    if user.is_authenticated:
        # filters wishlist product for user
        wishlists = WishlistProduct.objects.filter(user=user)

    # else if not authenticated and no session id for anonymous user 
    else:
        if not request.session.session_key:
            # creating new session for user
            request.session.create()
            
        # request for user session
        session_id = request.session.session_key
        
        try:
            # getting session for anonymous user
            session = Session.objects.get(session_key=session_id)
            
            # filtering wishlist for anonymous user
            wishlists = WishlistProduct.objects.filter(session=session)
        except Session.DoesNotExist:
            wishlists = []
    
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