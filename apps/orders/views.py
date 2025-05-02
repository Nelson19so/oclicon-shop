from django.shortcuts import render, redirect, get_object_or_404
from .forms import TrackOrderForm
from django.contrib import messages
from django.views.generic import ListView, DeleteView, View, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_http_methods
from .models import Order, OrderItem, OrderMessage
from apps.cart.models import Cart, CartItem
from apps.products.models import Product

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

    context = {"form": form}
        
    return render(request, 'pages/track_order.html', context)


# order details
class OrderDetails(DetailView):
    template_name = 'pages/order_details.html'
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

class CheckoutOrderViewCreate(View):
    @method_decorator(require_http_methods(["POST"]))
    def post(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('login')

        cart = Cart.objects.filter(user=user).first()
        if not cart:
            messages.error(request, "No items in cart.")
            return redirect('cart_view')  # or some cart view name

        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
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
        order.save()

        cart_items.delete()  # Optionally clear the cart
        return redirect('success_checkout')
