from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Order, OrderStatusHistory

# tracks changes in order status
@receiver(pre_save, sender=Order)
def track_order_status_changes(sender, instance, **kwargs):
    # checks for changes in order
    if not instance.pk:
        # returns nothing if no changes were made
        return

    # getting previous order
    previous = Order.objects.get(pk=instance.pk)

    # checks if the previous changes is not the same with the current changes
    if previous.status != instance.status:
        # creating new order status history
        OrderStatusHistory.objects.create(
            order=instance,
            old_status=previous.status,
            new_status=instance.status
        )
