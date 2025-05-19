from django.urls import path
from .views import (
    user_registration_view_create,
    logout_view, welcome_registration_view, 
    login_view, reset_password_view, 
    reset_password_request_view, 
    registration_email_verification,
    account_dashboard
)

urlpatterns = [
    #? user account
    path('dashboard/', account_dashboard, name='dashboard'),
    
    #? authentication
    path('register/', user_registration_view_create, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='user_logout'),
    path('welcome_user/<int:user_id>/', welcome_registration_view, name="welcome_user"),
    path('register/email_verification/', registration_email_verification, name='email_verify'),

    #? password reset
    path('login/reset-password/', reset_password_request_view, name='reset_password_request'),
    path('login/reset-password/reset/<uidb64>/<token>/', reset_password_view, name='reset_password_confirm'),

    # path('login/reset-password/sent/', views.password_reset_email_sent, name='password_reset_email_sent'),
    # path('login/reset-password/success/', views.password_reset_success, name='password_reset_success'),
    # path('login//invalid/', views.password_reset_invalid, name='password_reset_invalid'),
]
