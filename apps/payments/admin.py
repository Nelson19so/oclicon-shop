from django.contrib import admin
from .models import TempPayment

@admin.register(TempPayment)
class TempPaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'reference', 'amount', 'verified', 'created_at']

    def has_add_permission(self, request):
        return False
    