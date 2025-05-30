from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ProfilePicture, AdditionalUserInfo, BillingAddress
from django.utils.translation import gettext_lazy as _

# custom user
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('Name', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    readonly_fields = ('pk', 'date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('Name', 'password')}),
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
            'fields': ('email', 'Name', 'terms_accepted', 'password1', 'password2'),
        }),
    )

    search_fields = ('Name', 'email')
    ordering = ('Name',)

# user additional information
@admin.register(AdditionalUserInfo)
class AdditionalUserInfoAdmin(admin.ModelAdmin):
    fields = (
        'user', 'username', 
        'email', 'phone_number', 
        'city', 'zip_code', 
        'country_region'
    )
    list_display = ('user', 'username', 'email', 'phone_number',)
    list_filter = ('username', 'email', 'phone_number',)
    readonly_fields = ['updated_at']
    search_fields = ('username', 'email')

# user profile picture/avatar
@admin.register(ProfilePicture)
class ProfilePicture(admin.ModelAdmin):
    fields = ('user', 'profile')
    list_display = ('user', 'profile')
    list_filter = ('user', 'profile')
    readonly_fields = ['updated_at']
    search_fields= ['user']

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
