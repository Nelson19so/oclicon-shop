from django.db.models.signals import post_save
from django.dispatch import receiver
from src.apps.products.models import Category
from .seed_categories import seed_categories

@receiver(post_save, sender=Category)
def category_created_handler(sender, instance, created, **kwargs):
    if created:
        print(f"📦 New Category Created: {instance.name}")
        seed_categories()
