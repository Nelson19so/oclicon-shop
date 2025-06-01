from django.db import models
from apps.products.models import Product
from django.conf import settings
from django.contrib.sessions.models import Session
from decimal import Decimal

# cart
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_id', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"
    
    def total_price(self):
        total = Decimal('0.00')
        for item in self.cartitem_set.all():
            total += item.product.base_price * item.quantity
        return total

# cart item
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cart')
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} in Cart {self.cart.id}"
    
    # sub total price
    @property
    def sub_total_price(self):
        return self.product.base_price * self.quantity

# wishlist product model
class WishlistProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='wish_product')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_wish', blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-added_at']

    def __str__(self):
        identifier = self.user if self.user else self.session
        return f"{identifier} - {self.product}"
