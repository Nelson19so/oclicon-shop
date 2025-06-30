from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.utils import timezone

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
    username = None
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
    
# user profile
class ProfilePicture(models.Model):
    user = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE, related_name='profile', 
    )
    profile = models.ImageField(
        upload_to='profile', 
        blank=False, null=False,
        default='profile/default_profile_pic/icon-avatar.png'
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.Name}"

class UserStatus(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False, blank=True, null=True)
    is_banned = models.BooleanField(default=False, blank=True, null=True)
    ban_reason = models.TextField(max_length=500, blank=True, null=True)
    date_status = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.Name}"

# vendor modal
class UserVendor(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    category = models.ForeignKey('products.Category', on_delete=models.PROTECT)
    is_vendor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.Name}"

# vendor information
class VendorInformation():
    vendor = models.OneToOneField(UserVendor, on_delete=models.CASCADE)
    about_vendor = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.vendor}"

class TermsPrivacy(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    terms_privacy = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.Name}"

class AdditionalUserInfo(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='additional_user')
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    country_region = models.CharField(max_length=300, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.Name}"
    
    def is_complete(self):
        return all([
            self.email,
            self.phone_number,
            self.city,
            self.zip_code,
            self.country_region,
            self.username
        ])

# billing information
class BillingAddress(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='billing_info')
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

