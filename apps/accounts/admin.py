from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('pk', 'Name', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    readonly_fields = ('pk', 'date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('Name', 'password')}),
        (_('Personal Info'), {'fields': ('email', 'terms_accepted')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'Name', 'terms_accepted', 'password1', 'password2'),
        }),
    )

    search_fields = ('Name', 'email')
    ordering = ('Name',)
