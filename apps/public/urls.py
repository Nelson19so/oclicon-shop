from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home_page, name="home"),
  path('shop/', views.shop_page, name="shop")
]