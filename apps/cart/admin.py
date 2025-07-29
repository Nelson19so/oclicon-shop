from django.contrib import admin
from .models import Cart, CartItem, WishlistProduct, CartProductSpec


# Cart admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    fields = ('user', 'session_key')
    list_display = ('user', 'session_key', 'created_at',) 
    list_filter = ('user', 'created_at',)
    readonly_fields = ('id', 'created_at',)


admin.site.register(CartProductSpec)
class CartProductSpecInline(admin.TabularInline):
    model = CartProductSpec
    fields = ('memory', 'size', 'storage')


# Cart item admin
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    fields = ('cart', 'product', 'quantity', 'updated_at')
    list_display = ('cart', 'product', 'quantity', 'added_at', 'updated_at')
    list_filter = ('cart', 'added_at')
    readonly_fields = ['added_at', 'updated_at']
    inlines = [CartProductSpecInline]


@admin.register(WishlistProduct)
class WishlistProductAdmin(admin.ModelAdmin):
    fields = ('user', 'product')
    list_display = ('user', 'session_key', 'product', 'added_at')
    list_filter = ('user', 'added_at')
    readonly_fields = ('added_at', 'session_key')
