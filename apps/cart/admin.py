from django.contrib import admin
from .models import Cart, CartItem, WishlistProduct

# Cart admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    fields = ('user', 'session')
    list_display = ('user', 'session', 'created_at',) 
    list_filter = ('user', 'created_at',)
    readonly_fields = ('id', 'created_at',)

# Cart item admin
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    fields = ('cart', 'product', 'quantity', 'updated_at')
    list_display = ('cart', 'product', 'quantity', 'added_at', 'updated_at')
    list_filter = ('cart', 'added_at')
    readonly_fields = ['added_at', 'updated_at']

@admin.register(WishlistProduct)
class WishlistProductAdmin(admin.ModelAdmin):
    fields = ('user', 'product')
    list_display = ('user', 'session', 'product', 'added_at')
    list_filter = ('user', 'added_at')
    readonly_fields = ('added_at', 'session')
