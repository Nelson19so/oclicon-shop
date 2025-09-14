from django.shortcuts import render, redirect, get_object_or_404
from .forms           import TrackOrderForm
from django.contrib   import messages
from django.views.generic import View, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from .models          import (
    Order, OrderItem, OrderMessage, OrderStatusHistory, OrderProductSpec
)
from apps.cart.models import Cart, CartItem
from django.urls      import reverse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.utils.timezone import now
from django.db        import IntegrityError


# track user order page view
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
    context = {
        "form":        form, 
        'breadcrumbs': breadcrumbs
    }

    # renders template with context
    return render(request, 'orders/track_order.html', context)


# cancel user order
def cancel_order(request, order_id):
    # checks if user is authenticated
    if request.user.is_authenticated:
        # getting order and renders 404 if none is found
        order = get_object_or_404(Order, user=request.user, order_id=order_id)

        # makes sure the order is not yet shipped or not yet late
        if order.status in ['DELIVERED', 'ON_THE_ROAD', 'CANCELLED']:
            # sends user massage if order cant be canceled
            messages.error(request, 'Order cannot be canceled with current status')
            return redirect('order_details', order_id)

        # if order status test passes then the order is canceled
        order.status = 'CANCELLED'
        order.canceled_at = now()
        order.canceled_by = request.user
        order.save()

        messages.success(request, "Your order has been cancelled.")
        return redirect('order-history')

    return redirect('order-history')


# order details page view 
class OrderDetails(DetailView):
    template_name = 'orders/order_details.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        # getting the user order-id
        order_id = self.kwargs.get('order_id')

        try:

            order = get_object_or_404(
                Order, user=self.request.user, order_id=order_id
            )

        except Order.DoesNotExist:
            return redirect('order-history')

        # returning order with the id
        return order

    # filters all order status history by order id
    def get_order_status(self, order):

        try:

            # Get all the history records for the given order, sorted by time
            history_qs = OrderStatusHistory.objects.filter(order=order).order_by('changed_at')

            if not history_qs.exists():
                return [order.status]  # fallback if there's no history

            status_chain = []

            # Add the initial old_status of the first record (first known status)
            first_status = history_qs.first().old_status

            if first_status:
                status_chain.append(first_status)

            # Then add all new_status in order
            for history in history_qs:
                if history.new_status and history.new_status not in status_chain:
                    status_chain.append(history.new_status)

            return status_chain[:1]

        except Exception as e:
            print("Error:", e)
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the order from the get object
        order = self.get_object()

         # Get the order items
        context['order_items'] = OrderItem.objects.filter(order=order)

        # Get all messages related to the order
        context['order_messages'] = OrderMessage.objects.filter(order=order)

        # Get all order status
        context['order_status'] = self.get_order_status(order)
        
        return context


# adding items to order | place order for user
class CheckoutOrderViewCreate(View):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('login')

        try:

            cart = Cart.objects.get(user=user)

        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)
        
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
            order_item = OrderItem.objects.create(
                order=order,
                price=item.product.base_price,
                product=item.product,
                quantity=item.quantity,
            )
            
            try:
                
                OrderProductSpec.objects.create(
                    order_item=order_item,
                    memory=item.cart_prod_spec.memory,
                    size=item.cart_prod_spec.size,
                    storage=item.cart_prod_spec.storage,
                )
                
            except IntegrityError:
                order.delete()
                return redirect('cart_list')

            total_amount += item.quantity * item.product.base_price

        order.total_amount = total_amount
        order.save()

        # delete all cart item after order is placed
        cart_items.delete()
        cart_key = f'cart_user_{request.user.id}'
        cache.delete(cart_key)

        request.session['order_id'] = order.order_id
        request.session['order_placed_success'] = True
        
        return redirect('order_successfully_placed', order.order_id)


# checkout view
@login_required(login_url='login')
def checkout_view(request):
    cart_item = []
    
    try:
        
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.filter(cart=cart).exists
        
    except (Cart.DoesNotExist or CartItem.DoesNotExist):
        pass
    
    if cart_item:
        breadcrumbs = [
            ('Shopping Cart', reverse('cart_list')),
            ('Checkout', request.path)
        ]

        context = {'breadcrumbs': breadcrumbs}
        return render(request, 'orders/checkout.html', context)
    return redirect('cart_list')


# successfully placed order view
def successfully_placed_order_view_create(request, order_id):
    if request.user.is_authenticated:
        if request.session.get('order_placed_success'):

            # checks if the session order id matches with the session id
            if request.session.get('order_id') != str(order_id):
                return redirect('home')
            
            order_id_ = request.session.get('order_id')

            # clear session for order
            request.session.pop('order_id', None)
            request.session.pop('order_placed_success', None)
            
            return render(request, 'orders/order_successfully_Placed.html', {
                "order_id_": order_id_
            })
        return redirect('dashboard')
    return redirect('home')

