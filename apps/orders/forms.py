from django import forms
from .models import Order, OrderItem, ShippingAddress

class TrackOrderForm(forms.Form):
    email = forms.EmailField()
    order_id = forms.CharField()

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        order_id = cleaned_data.get("order_id")
        email = cleaned_data.get("email")

        if order_id and email:
            try:
                Order.objects.get(user=self.user, email=email, order_id=order_id)
            except Order.DoesNotExist:
                raise forms.ValidationError("No order was found for this user with the " \
                "provided email and order id")
        else:
            raise forms.ValidationError('Make sure order and email input is valid')
        return cleaned_data

# shipping address model form
class ShippingAddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ['user']