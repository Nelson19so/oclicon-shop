from django.urls import path
from .views.auth_view import (
    user_registration_view_create, reset_user_password,
    logout_view, welcome_registration_view, 
    login_view, reset_password_view, 
    reset_password_request_view, 
    registration_email_verification, 
    user_successfully_logged_out,
)
from .views.account_view import (
    order_history, user_settings_profile,
    delete_user_account, search_history,
    account_dashboard, card_address,
)

urlpatterns = [
    #? user account
    path('dashboard/', account_dashboard, name='dashboard'),
    path('order-history/', order_history, name='order-history'),
    path('card-address/', card_address, name='card-address'),
    path('search_history/', search_history, name='search-history'),
    path('profile_settings/', user_settings_profile, name='profile'),
    path('delete_user/', delete_user_account, name='delete_user'),

    #? authentication
    path('register/', user_registration_view_create, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('welcome_user/<int:user_id>/', welcome_registration_view, name="welcome_user"),
    path('register/email_verification/', registration_email_verification, name='email_verify'),
    path('successful_logout/', user_successfully_logged_out, name='successful_logout'),
    path('reset_user_password/', reset_user_password, name='reset_user_password'),

    #? password reset
    path('login/reset-password/', reset_password_request_view, name='reset_password_request'),
    path('login/reset-password/reset/<uidb64>/<token>/', reset_password_view, name='reset_password_confirm'),

    # path('login/reset-password/sent/', views.password_reset_email_sent, name='password_reset_email_sent'),
    # path('login/reset-password/success/', views.password_reset_success, name='password_reset_success'),
    # path('login//invalid/', views.password_reset_invalid, name='password_reset_invalid'),
]
