from django.shortcuts import render, get_object_or_404, redirect
from apps.products.models import Product
from .models import Cart, CartItem, WishlistProduct
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, View
from django.contrib.sessions.models import Session
from django.http import HttpResponseNotAllowed

# Create your views here.

class CartMixin:
    def cart_item_count(self, request):
        user = request.user

        if user.is_authenticated:
            return CartItem.objects.filter(user=user).count()
        
        if not request.session.session_key:
            return 0

        return CartItem.objects.filter(cart__session__session_key=request.session.session_key).count()


    def cart_items_list(self, request):
        user = request.user
        session_id = request.session.session_key

        if user.is_authenticated:
            cart = Cart.objects.filter(user=user).first()
            if cart:
                return CartItem.objects.filter(cart=cart)
            else:
                return CartItem.objects.none()

        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        cart = Cart.objects.filter(session__session_key=session_id).first()

        if cart:
            return CartItem.objects.filter(cart=cart)
        else:
            return CartItem.objects.none()

        
class CreateCartItem(CartMixin, View):
    @method_decorator(require_http_methods([require_POST]))
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs.get('product_slug'))
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
            cart, created = Cart.objects.get_or_create(session=session)
            cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)

            if not created:
                cart_item.quantity = 1
                cart_item.save()

        return JsonResponse({
            'status': 'success',
            'count': self.cart_item_count(request)
        })

class RemoveItemFromCart(View):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        cart_id = kwargs.get('cart_id')
        user = request.user
        session_id = request.session.session_key

        if user.is_authenticated:
            cart_item = get_object_or_404(CartItem, car__user=user, id=cart_id)

        else:
            if not session_id:
                request.session.create()
                session_id = request.session_key

                cart_item = get_object_or_404(CartItem, car__session=session_id, id=cart_id)
        
        cart_item.delete()

class CartItemListView(CartMixin, ListView):
    template_name = "pages/cart.html"
    context_object_name = "cart"

    def get_queryset(self):
        return self.cart_items_list(self.request)

# update cart product quantity view create
@require_POST
def update_cart_quantities(request):
    user = request.user

    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart = Cart.objects.filter(session=session_id).first()

    if not cart:
        return redirect('cart_list')

    # Loop through posted quantities
    for item_id, quantity in request.POST.items():
        try:
            quantity = int(quantity)
            quantity = quantity
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.quantity = quantity
            cart_item.save()
        except:
            pass

    return redirect('cart_list')

# product wishlist view create
class WishListProductCreate(View):
    @method_decorator(require_http_methods(["POST"]))
    def post(self, request, *args, **kwargs):
        user = request.user
        session_id = request.session.session_key
        product_slug = kwargs.get('product_id')

        product = get_object_or_404(Product, slug=product_slug)

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

class RemoveItemFromWishlist(View):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs.get('product_id'))
        user = request.user

        if user.is_authenticated:
            WishlistProduct.objects.filter(user=user, product=product).delete()
        else:
            session_id = request.session.session_key
            WishlistProduct.objects.filter(session=session_id, product=product).delete()

        return JsonResponse({
            'status': 'success',
            'message': 'Product removed from wishlist'
        })

def wish_list_view(request):
    user = request.user
    session_id = request.session.session_key
    
    if user.is_authenticated:
        wishlist = WishlistProduct.objects.filter(user=user)
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    wishlist = WishlistProduct.objects.filter(session=session_id)
    
    context = {"wishlist": wishlist, "user": user}
    return render(request, 'pages/wishlist.html', context)