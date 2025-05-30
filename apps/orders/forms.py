from django import forms
from .models import Order, OrderItem, ShippingAddress

class TrackOrderForm(forms.Form):
    email = forms.EmailField()
    order_id = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        order_id = cleaned_data.get("order_id")
        email = cleaned_data.get("email")

        try:
            if not Order.objects.filter(email=email):
                forms.ValidationError("Email does not match the order ID provided")
            if not Order.objects.filter(order_id=order_id):
                forms.ValidationError("The order id you provided was not found")
        except Order.DoesNotExist:
            forms.ValidationError("Order you provided not found")       

# shipping address model form
class ShippingAddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ['user']