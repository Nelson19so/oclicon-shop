from django.db import models
from django.conf import settings
from apps.cart.models import CartItem
import random


def create_random_order_id():
    return ''.join(random.choices('0123456789', k=10))

# user order model
class Order(models.Model):
    ORDER_STATUS = (
        ('ORDER_PLACED', 'Order Placed'),
        ('PACKAGING', 'Packaging'),
        ('ON_THE_ROAD', 'On the Road'),
        ('CANCELLED', 'Cancelled'),
        ('PENDING', 'Pending'),
        ('DELIVERED', 'Delivered'),
    )

    order_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    canceled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    canceled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.get_status_display()}"
    
    @property
    def order_status(self):
        return f'{self.get_status_display()}'
    
    @property
    def quantity(self):
        total_product = 0
        for item in self.items.all():
            total_product += item.quantity
        return f'{total_product}'
    
    def total_product(self):
        total_product = 0
        for item in self.items.all():
            total_product += item.quantity
        return f'{total_product} Product'
    
    def save(self, *args, **kwargs):
        if not self.email:
            self.email = self.user.email
        
        if not self.order_id:
            super().save(*args, **kwargs)  # Save to get an `id`
            prefix = "033"
            self.order_id = f"{prefix}{str(self.id).zfill(7)}"
            kwargs['force_insert'] = False  # Prevent insert error

        return super().save(*args, **kwargs)


# order items model for product
class OrderItem(models.Model):
    product = models.ForeignKey(
        'products.Product', on_delete=models.CASCADE, null=False, blank=False
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items', null=False, blank=False
    )
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


# Order product specification model
class OrderProductSpec(models.Model):
    memory = models.CharField(blank=True, null=True)
    size = models.CharField(blank=True, null=True)
    storage = models.CharField(blank=True, null=True)
    order_item = models.OneToOneField(
        OrderItem, on_delete=models.CASCADE, related_name='order_item_spec'
    )

    class Meta:
        unique_together = ('memory', 'size', 'storage')


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.old_status} → {self.new_status} on {self.changed_at}"

# order messages
class OrderMessage(models.Model):
    message = models.CharField(max_length=255)
    date_sent = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f"Message for Order {self.order.order_id}"

# shipping address
class ShippingAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shipping_info')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=400, null=True, blank=True)
    address = models.CharField(max_length=500)
    country = models.CharField(max_length=200)
    zip_code = models.IntegerField()
    region_state = models.CharField(max_length=300)
    city = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name}"

    @property
    def full_name(self):
        return f"{self.first_name + ' ' + self.last_name}"