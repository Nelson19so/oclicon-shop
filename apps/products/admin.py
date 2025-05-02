from django.contrib import admin
from .models import *

# Register your models here.

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('color', 'stock', 'price_adjustment', 'is_default')

class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 1

class BadgeVariantInLine(admin.TabularInline):
    model = Badge
    list_display = ('bade_type', 'is_active',)
    list_filter = ('name', 'bade_type', 'show_percentage', 'is_active',)
    extra = 1

@admin.register(Badge)
class Badge(admin.ModelAdmin):
    list_display = ('bade_type', 'is_active')
    list_filter = ('bade_type', 'is_active')
    # list_display = ('bade_type', 'product')
    # list_filter = ('bade_type', 'product')

@admin.register(ProductComparison)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_id', 'product', 'added_date')

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'current_price', 'is_active')
    list_filter = ['brand', 'category', 'is_active']
    search_fields = ('name', 'sku', 'description')
    # prepopulated_fields = {'slug': ('name',)}
    exclude = ['slug']
    inlines = [ProductVariantInline, ProductImageInLine]

@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_color')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', 'parent')
    list_filter = ['name', 'parent']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ('name', 'logo')
    list_filter = ['name', 'logo']
    exclude = ['slug']