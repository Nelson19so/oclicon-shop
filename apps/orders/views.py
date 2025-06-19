from django.shortcuts import render, redirect, get_object_or_404
from .forms import TrackOrderForm
from django.contrib import messages
from django.views.generic import ListView, DeleteView, View, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_http_methods
from .models import Order, OrderItem, OrderMessage, OrderStatusHistory
from apps.cart.models import Cart, CartItem
from apps.products.models import Product
from django.urls import reverse
from datetime import timezone
from django.contrib.auth.decorators import login_required

# track user order page
def track_order(request):
    # request for the authenticated user 
    user = request.user
    
    # Handles post request from users
    if request.method == "POST":

        # checks if user is authenticated
        if user.is_authenticated:
            form = TrackOrderForm(request.user, request.POST)

            # checks if form is valid
            if form.is_valid():
                # getting the order id from the data submit by the user
                order_id = form.cleaned_data["order_id"]
                
                # redirect user to the order details page with the order id provided by user
                return redirect('order_details', order_id=order_id)

        # if user is not authenticated
        else:
            # redirect users to login
            return redirect('login')
    else:
        form = TrackOrderForm()

    # builds breadcrumb for this page
    breadcrumbs = [
        ('Track Order', request.path)
    ]

    # context for use in template
    context = {"form": form, 'breadcrumbs': True, 'breadcrumbs': breadcrumbs}
    # renders template with context
    return render(request, 'orders/track_order.html', context)

# cancel user order
def cancel_order(request, order_id):
    # checks if user is authenticated
    if request.user.is_authenticated:
        # getting order and renders 404 if none is found
        order = get_object_or_404(Order, id=order_id)
        
        # makes sure the order is not yet shipped or not yet late
        if order.status in ['_']:
            # sends user massage if order cant be canceled
            messages.error(request, 'Order cannot be canceled with current status')
            return redirect('order-list')

        # if order status test passes then the order is canceled
        order.status == 'CANCELLED'
        order.canceled_at = timezone.now()
        order.canceled_by = request.user
        order.save()
    
        messages.success(request, "Your order has been cancelled.")
        return redirect('order-list')
        
    return redirect('order-list')

# order details
class OrderDetails(DetailView):
    template_name = 'orders/order_details.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        # getting order id
        order_id = self.kwargs.get('order_id')

        # returning order with the id
        return get_object_or_404(Order, order_id=order_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the order from the get object
        order = self.get_object()

         # Get the order items
        context['order_items'] = OrderItem.objects.filter(order=order)

        # order history status
        context['order_history'] = OrderStatusHistory.objects.filter(order=order)
        
        # Get all messages related to the order
        context['order_messages'] = OrderMessage.objects.filter(order=order)
        return context

# adding items to order | place order for user
class CheckoutOrderViewCreate(View):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('login')

        cart = Cart.objects.get(user=user)
        # if the cart doesn't exist
        if not cart:
            return redirect('cart_list')  # or some cart view name

        cart_items = CartItem.objects.filter(cart=cart)
        # if cart item doesn't exist
        if not cart_items.exists():
            return redirect('cart_list')

        order = Order.objects.create(user=user, total_amount=0)
        total_amount = 0

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.base_price
            )
            total_amount += item.quantity * item.product.base_price

        order.total_amount = total_amount
        order = order.save()

        # delete all cart item after order is placed
        cart_items.delete() 

        # request.session['order_id'] = order.id
        # request.session['order_placed_success'] = True
        
        # return redirect('success_checkout', order.id)

        return redirect('checkout')

# checkout view
@login_required(login_url='login')
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

