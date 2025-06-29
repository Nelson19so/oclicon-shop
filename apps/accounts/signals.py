from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ProfilePicture

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_default_profile_picture(sender, instance, created, **kwargs):
    if created:
        ProfilePicture.objects.create(
          user=instance,
          profile='profile/default_profile_pic/icon-avatar.png'
    )
