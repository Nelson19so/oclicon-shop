from django.db import models
from apps.products.models import Product
from django.conf import settings
import random

def create_random_order_id():
    return ''.join(random.choices('0123456789', k=10))

class Order(models.Model):
    ORDER_STATUS = (
        ('ORDER_PLACED', 'Order Placed'),
        ('PACKAGING', 'Packaging'),
        ('ON_THE_ROAD', 'On the Road'),
        ('CANCELLED', 'Cancelled'),
        ('SHIPPED', 'Shipped'),
        ('PENDING', 'Pending'),
        ('DELIVERED', 'Delivered'),
    )

    order_id = models.CharField(max_length=10, unique=True, default=create_random_order_id)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')

    def __str__(self):
        return f"Order {self.order_id}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class OrderMessage(models.Model):  # Renamed to singular "OrderMessage"
    message = models.CharField(max_length=255)
    date_sent = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f"Message for Order {self.order.order_id}"
