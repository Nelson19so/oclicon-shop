from django.contrib import admin
from .models import *

class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    fields = ('image', 'is_featured', 'order')
    ordering = ['order']
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    fields = ('color', 'stock', 'price_adjustment', 'is_default')
    extra = 1

class BadgeVariantInLine(admin.TabularInline):
    model = Badge
    list_display = ('bade_type', 'is_active',)
    list_filter = ('name', 'bade_type', 'show_percentage', 'is_active',)
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    fields = ('memory', 'size', 'storage')
    extra = 1

class BadgeInline(admin.TabularInline):
    model = Badge
    fields = ('bade_type', 'is_active')
    extra = 1

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('bade_type', 'product', 'is_active')
    list_filter = ('bade_type', 'is_active')

@admin.register(ProductComparison)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_id', 'product', 'added_date')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = (
        'name', 'brand', 
        'category', 'base_price', 
        'discount_price', 'description', 
        'is_active', 'slug'
    )
    list_display = ('name', 'brand', 'current_price', 'is_active', 'average_rating')
    list_filter = ['brand', 'category', 'is_active']
    search_fields = ('name', 'sku', 'description')
    # prepopulated_fields = {'slug': ('name',)}
    exclude = ('slug', 'skull')
    readonly_fields = ('id', 'created_at', 'updated_at', 'slug')
    inlines = [
        ProductVariantInline, BadgeInline,
        ProductImageInLine, ProductSpecificationInline
    ]

@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_color')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    fields = ('id', 'name', 'parent', 'slug')
    list_display = ('name', 'parent')
    list_filter = ['name', 'parent']
    readonly_fields = ('slug', 'id')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ('name', 'logo')
    list_filter = ['name', 'logo']
    exclude = ['slug']

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    fields = (
        'title', 'name', 
        'description', 'image', 
        'url', 'position', 
        'is_active', 'price', 
        'badge', 'highlight'
    )
    list_display = ('name', 'title', 'position', 'is_active')
    list_filter = ('name', 'title', 'position', 'is_active')
    readonly_fields = ['created_at']

@admin.register(ProductHighlight)
class ProductHighlightAdmin(admin.ModelAdmin):
    fields = ('product', 'features', 'date_created', 'is_active', 'updated_at')
    list_display = ('product', 'features', 'date_created', 'is_active')
    list_filter = ('features', 'date_created', 'is_active')
    readonly_fields = ('id', 'date_created', 'updated_at')
    search_fields = ['features']

# product rating
@admin.register(ProductRating)
class ProductRateAdmin(admin.ModelAdmin):
    fields = ('user', 'product', 'stars', 'review', 'date_created')
    list_display = ('user', 'product', 'stars', 'date_created')
    list_filter = ('user', 'stars', 'date_created')
    readonly_fields = ('id', 'date_created')
