from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.

# base user model
class BaseUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('email field is required')
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email, password, **extra_fields)

# Custom user model
class CustomUser(AbstractUser):
    Name = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, max_length=200)
    terms_accepted = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['Name', 'terms_accepted']

    objects = BaseUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.Name
    

