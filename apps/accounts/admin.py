from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ProfilePicture, AdditionalUserInfo, BillingAddress, UserStatus
from django.utils.translation import gettext_lazy as _

# custom user
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    readonly_fields = ('pk', 'date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('email', 'terms_accepted')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 
            'is_superuser', 'groups', 
            'user_permissions'
        )}),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'terms_accepted', 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)

# user additional information
@admin.register(AdditionalUserInfo)
class AdditionalUserInfoAdmin(admin.ModelAdmin):
    fields = (
        'user', 'related_username', 
        'second_email', 'phone_number', 
        'city', 'zip_code', 
        'country_region'
    )
    list_display = ('user', 'related_username', 'second_email', 'phone_number',)
    list_filter = ('related_username', 'second_email', 'phone_number',)
    readonly_fields = ['updated_at']
    search_fields = ('related_username', 'second_email')

# user profile picture/avatar
@admin.register(ProfilePicture)
class ProfilePicture(admin.ModelAdmin):
    fields = ('user', 'profile')
    list_display = ('user', 'profile', 'updated_at')
    list_filter = ('user', 'profile', 'updated_at')
    readonly_fields = ['updated_at']
    search_fields = ['user']

@admin.register(BillingAddress)
class BillingAddress(admin.ModelAdmin):
    fields = (
        'user', 'first_name', 
        'last_name', 'company_name', 
        'address', 'country', 
        'zip_code', 'region_state', 
        'city', 'email', 
        'phone_number'
    )
    list_display = (
        'full_name', 'country', 
        'region_state', 'city', 
        'zip_code', 'email'
    )
    list_filter = (
        'first_name', 'last_name', 
        'country', 'region_state', 
        'city', 'zip_code',
        'email'
    )
    readonly_fields = ('id', 'updated_at')

@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    fields = ('user', 'is_verified', 'is_banned', 'ban_reason')
    list_display = ('user', 'is_verified', 'is_banned', 'date_status')
    list_filter = ('user', 'is_verified', 'is_banned', 'date_status')
    search_fields = ['user']
    readonly_fields = ['date_status']
