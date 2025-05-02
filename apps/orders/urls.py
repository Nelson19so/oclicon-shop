from django.urls import path
from .views import OrderDetails, track_order

urlpatterns = [
    path('track_order/', track_order, name='track_order'),
    path('track_order/order_details/<str:order_id>/', OrderDetails.as_view(), name='order_details')
]