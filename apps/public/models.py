from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    full_name = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child')
    message = models.TextField(max_length=300, blank=False, null=False)
    created_at = models.DateTimeField(default=True)

    def __str__(self):
        return f"{self.full_name}"

class NewsLetterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(default=True)

    def __str__(self):
        return f"{self.email} subscribed at {self.subscribed_at}"

class cliconTeamMember(models.Model):
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    profile = models.ImageField(upload_to='team/', blank=False, null=False)

    def __str__(self):
        return f"{self.full_name} role {self.role}"