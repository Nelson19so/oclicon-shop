from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.conf import settings

# Create your models here.

# brand model
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
          self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
  
# category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def save(self, *args, **kwargs):
        if not self.slug:
          self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  
  
# product model
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    sku = models.CharField(max_length=20, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    category = models.ManyToManyField(Category)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug

            num = 1
            while Product.objects.filter(slug=unique_slug).exists():
              unique_slug = f"{base_slug}-{num}"
            self.slug = unique_slug
        super().save(*args, **kwargs)

    @property
    def current_price(self):
        return self.discount_price if self.discount_price else self.base_price
    
    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.sku})"
    
# product colors type
class ProductColor(models.Model):
    name = models.CharField(max_length=20)
    hex_color = models.CharField(max_length=7, help_text='E.G., #FFF')

    def __str__(self):
        return self.name

# products specifications 
class ProductSpecification(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# product badge
class Badge(models.Model):
    BADGE_TYPE = [
        ('sale', 'SALE'),
        ('hot', 'HOT'),
        ('new', 'NEW'),
        ('bestdeal', 'BEST DEAL')
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_badge')
    bade_type = models.CharField(max_length=20, choices=BADGE_TYPE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bade_type}"
  
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variant')
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, null=True, blank=True)
    product_specification = models.ForeignKey(ProductSpecification, on_delete=models.PROTECT, null=True, blank=True)
    badge = models.ManyToManyField(Badge)
    stock = models.PositiveIntegerField(default=0)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_default = models.BooleanField(default=False)

    @property
    def final_price(self):
        return self.product.current_price + self.price_adjustment
    
    @property
    def availability(self):
        if self.stock > 20:
            return "In Stock"
        elif self.stock > 1:
            return f"Only {self.stock} Left"
        return "Out of Stock"

    def __str__(self):
        return f"{self.product.name} - {self.color} {self.product_specification}"

class ProductImage(models.Model):
    variant = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.variant}"
  
# product comparison
class ProductComparison(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productcomparison')
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session_id', 'product')

    def __str__(self):
        return f"{self.product.name}"
    