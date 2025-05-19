from django.shortcuts import render, redirect, get_object_or_404
from .forms import TrackOrderForm
from django.contrib import messages
from django.views.generic import ListView, DeleteView, View, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_http_methods
from .models import Order, OrderItem, OrderMessage
from apps.cart.models import Cart, CartItem
from apps.products.models import Product
from django.urls import reverse

# Create your views here.

def track_order(request):
    user = request.user
    
    if request.method == "POST":
        if user.is_authenticated:
            form = TrackOrderForm(request.POST)
            print(request.POST)
            if form.is_valid():
                order_id = form.cleaned_data["order_id"]

                return redirect('order_details', order_id=order_id)
        else:
            return redirect('login')
    else:
        form = TrackOrderForm()

    breadcrumbs = [
        ('Track Order', request.path)
    ]
    
    context = {"form": form, 'breadcrumbs': True, 'breadcrumbs': breadcrumbs}
    return render(request, 'orders/track_order.html', context)


# order details
class OrderDetails(DetailView):
    template_name = 'orders/order_details.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        order_id = self.kwargs.get('order_id')
        return get_object_or_404(Order, order_id=order_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        
         # Get the order items
        context['order_items'] = OrderItem.objects.filter(order=order)
        
        # Get all messages related to the order
        context['order_messages'] = OrderMessage.objects.filter(order=order)
        return context

# adding items to order
class CheckoutOrderViewCreate(View):
    @method_decorator(require_http_methods(["POST"]))
    def post(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('login')

        cart = Cart.objects.filter(user=user).first()
        # if the cart doesn't exist
        if not cart:
            return redirect('cart_view')  # or some cart view name

        cart_items = CartItem.objects.filter(cart=cart)
        # if cart item doesn't exist
        if not cart_items.exists():
            return redirect('cart_view')

        order = Order.objects.create(user=user, total_amount=0)
        total_amount = 0

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total_amount += item.quantity * item.product.price

        order.total_amount = total_amount
        order = order.save()

        cart_items.delete()  # Optionally clear the cart

        request.session['order_id'] = order.order_id
        request.session['order_placed_success'] = True
        
        return redirect('success_checkout', order.order_id)

# checkout view
def checkout_view(request):
    breadcrumbs = [
        ('Shopping Cart', reverse('cart_list')),
        ('Checkout', request.path)
    ]
    
    context = {'breadcrumbs': breadcrumbs}
    return render(request, 'orders/checkout.html', context)

# successfully placed order view
def successfully_placed_order_view_create(request, order_id):
    if request.user.is_authenticated:
        if request.session.get('order_placed_success'):

            # checks if the session order id matches with the session id
            if request.session.order_id != order_id:
                return redirect('home')
            
            order_id_ = request.session.get('order_id')

            # clear session for order
            request.session.pop('order_id', None)
            request.session.pop('order_placed_success', None)
            
            return render(request, 'orders/order_successfully_Placed.html', {"order_id_": order_id_})
        return redirect('dashboard')
    return redirect('home')

# def successfully_placed_order_view_create(request):
#     return render(request, 'orders/order_successfully_Placed.html')