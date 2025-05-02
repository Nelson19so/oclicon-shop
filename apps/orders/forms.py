from django import forms
from .models import Order, OrderItem

class TrackOrderForm(forms.Form):
    email = forms.EmailField()
    order_id = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        order_id = cleaned_data.get("order_id")
        email = cleaned_data.get("email")

        try:
            orders = Order.objects.filter(order_id=order_id)
            order = orders.first()
            
            if order.email != email:
                self.add_error("email", "Email does not match the order ID provided")
        except Order.DoesNotExist:
            self.add_error("order_id", "Order you provided not found")        