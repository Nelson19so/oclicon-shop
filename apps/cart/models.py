from django.db import models
from django.conf import settings
from apps.products.models import ProductSpecification
from decimal import Decimal

# cart model
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"
    
    def total_price(self):
        total = Decimal('0.00')
        for item in self.cartitem_set.all():
            total += item.product.base_price * item.quantity
        return total
    

# cart items model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(
        'products.Product', on_delete=models.PROTECT, related_name='product_cart'
    )
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('cart', 'product',)

    def __str__(self):
        return f"{self.product.name}"
    
    # sub total price
    @property
    def sub_total_price(self):
        return self.product.base_price * self.quantity


# cart product specification model
class CartProductSpec(models.Model):
    cart_item = models.OneToOneField(
        CartItem, on_delete=models.CASCADE, related_name='cart_prod_spec'
    )
    memory = models.CharField(blank=True, null=True)
    size = models.CharField(blank=True, null=True)
    storage = models.CharField(blank=True, null=True)

    class Meta:
        unique_together = ('memory', 'size', 'storage')

    def __str__(self):
        return f'{self.cart_item.product.name} - product cart specification'
        

# wishlist product model
class WishlistProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    product = models.OneToOneField('products.Product', on_delete=models.PROTECT, related_name='wish_product')
    session_key = models.CharField(max_length=40, null=True, blank=True) 
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-added_at']

    def __str__(self):
        identifier = self.user if self.user else self.session_key
        return f"{identifier} - {self.product}"
