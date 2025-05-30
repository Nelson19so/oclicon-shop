from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.conf import settings
import random
import string

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
  
# random skull for product
def create_product_random_skull():
    return ''.join(random.choices('0123456789Aabcdefghigklmnopqrstuvwxyz', k=10))

# product model
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    sku = models.CharField(max_length=20, unique=True, default=create_product_random_skull)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    category = models.ManyToManyField(Category, related_name='product_category')
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specification')
    memory = models.CharField(blank=True, null=True)
    size = models.CharField(blank=True, null=True)
    storage = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.product.name

# product badge
class Badge(models.Model):
    BADGE_TYPE = [
        ('sale', 'SALE'),
        ('hot', 'HOT'),
        ('new', 'NEW'),
        ('best_deal', 'BEST DEAL'),
        ('sold_out', 'SOLD OUT')
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_badge')
    bade_type = models.CharField(max_length=20, choices=BADGE_TYPE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bade_type}"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variant')
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, null=True, blank=True)
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
            return f"Only {self.stock} product Left"
        return "Out of Stock"

    def __str__(self):
        return f"{self.product.name} - {self.color}"

class ProductImage(models.Model):
    variant = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.variant}"
  
# ads for product
class Ad(models.Model):
    POSITION_CHOICES = [
        ('top', 'Top Banner'),
        ('bottom', 'Bottom Banner'),
        ('sidebar', 'Sidebar'),
        ('popup', 'Popup'),
        ('middle_banner', 'Middle Banner'),
    ]

    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='ads/')
    url = models.URLField(blank=True, null=True)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
  
# product Highlight
class ProductHighlight(models.Model):
    FEATURES = [
        ('best_deal', 'Best Deals'),
        ('featured_product', 'Featured Products'),
        ('flash_sale_today', 'FLASH SALE TODAY'),
        ('best_sellers', 'BEST SELLERS'),
        ('top_rated', 'TOP RATED'),
        ('new_arrival', 'NEW ARRIVAL')
    ]

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name='product_feature'
    )
    features = models.CharField(max_length=50, choices=FEATURES, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return f'{self.get_features_display}'

# product features
# class ProductFeature(models.Model):
#     variant = models.OneToOneField(
#         ProductVariant, on_delete=models.CASCADE, related_name='product_features'
#     )

# product comparison
class ProductComparison(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    session_id = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name='session', null=True, blank=True
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_comparison'
    )
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session_id', 'product')

    def __str__(self):
        return f"{self.product.name}"
    