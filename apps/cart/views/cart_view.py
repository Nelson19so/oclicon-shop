from django.shortcuts import get_object_or_404, redirect
from apps.products.models import Product
from apps.cart.models import Cart, CartItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View
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
    
    # calculate cart total amount for checkout taxes + cart items
    def calculate_cart_tax(self, request):
        cart_item_count = self.cart_item_count(self.request)
        sub_total = round(61.99 * cart_item_count, 2)
        return sub_total
        
    # get total price
    def get_total_price(self, request):
        cart = 0

        try:
            if request.user.is_authenticated:
                cart = Cart.objects.get(user=request.user)
            else:
                session_key = self.get_or_create_session_key(request)
                cart = Cart.objects.get(session_key=session_key)
            cart = cart.total_price
        except Cart.DoesNotExist:
            pass
        return cart
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        context['total_price'] = self.get_total_price(self.request)
        context['cart_shipping_sub_total'] = self.calculate_cart_tax(self.request)
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

            if quantity < 1:
                continue
            
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.quantity = quantity
            cart_item.updated_at = timezone.now()
            cart_item.save()
        except (ValueError, CartItem.DoesNotExist):
            # skip invalid entries silently
            continue

    return redirect('cart_list')
