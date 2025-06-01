from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem, OrderMessage, OrderStatusHistory

@admin.register(ShippingAddress)
class BillingAddress(admin.ModelAdmin):
    fields = (
        'user',
        'first_name', 
        'last_name',
        'company_name', 
        'address', 
        'country', 
        'zip_code', 
        'region_state',
        'city', 
        'email', 
        'phone_number'
    )
    list_display = ('full_name', 'country', 'region_state', 'city', 'zip_code', 'email')
    list_filter = ('first_name', 'last_name', 'country', 'region_state', 'city', 'zip_code', 'email')
    readonly_fields = ('id', 'updated_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('user', 'email', 'total_amount', 'status', 'order_id')
    list_display = ('order_id', 'user', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'email', 'user__email')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    exclude = ('canceled_at', 'canceled_by', 'order_id')
    readonly_fields = ('order_id', 'id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    fields = ('product', 'order', 'quantity', 'price')
    list_display = ('product', 'order', 'quantity', 'price')

@admin.register(OrderMessage)
class OrderMessageAdmin(admin.ModelAdmin):
    list_display = ('order', 'message', 'date_sent')

@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'old_status', 'new_status', 'changed_at']
    list_filter = ['new_status', 'changed_at']