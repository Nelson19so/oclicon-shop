from django.urls import path
from .views import register_view, logout_view

urlpatterns = [
    path('register/', register_view, name='use_registration'),
    path('logout/', logout_view, name='user_logout'),
]