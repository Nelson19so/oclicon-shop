from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings
from .models import ProfilePicture
from django.contrib.auth.models import User
import os
from django.core.files import File

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_default_profile_picture(sender, instance, created, **kwargs):
    if created:
        avatar = ProfilePicture.objects.create(
                      user=instance,
                      profile='profile/default_profile_pic/icon-avatar.png'
                  )
        if not avatar.profile:
            default_img_path = os.path.join(
                settings.BASE_DIR, 'static/default_profile_pic/icon-avatar.png'
            )
            media_img_path = os.path.join(
                settings.MEDIA_ROOT, 'profile/default_profile_pic/icon-avatar.png'
            )
            if not os.makedirs(os.path.dirname(media_img_path), exist_ok=True):
                with open(default_img_path, 'rb') as f:
                    with open(media_img_path, 'wb') as dest:
                        dest.write(f.read())
            avatar.profile.save('icon-avatar.png', File(open(media_img_path, 'rb')))
            avatar.save()

@receiver(user_logged_in)
def create_profile(sender, user, request, **kwargs):
    try:
        user.profile
    except ProfilePicture.DoesNotExist:
        profile = ProfilePicture.objects.create(
            user=user,
            profile='profile/default_profile_pic/icon-avatar.png'
        )
        profile.save()
