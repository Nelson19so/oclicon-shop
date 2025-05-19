from django.urls import path
from .views import OrderDetails, track_order, checkout_view, successfully_placed_order_view_create

urlpatterns = [
    path('track_order/', track_order, name='track_order'),
    path('track_order/order_details/<int:order_id>/', OrderDetails.as_view(), name='order_details'),

    # checkout
    path('checkout/', checkout_view, name='checkout'),
    path("order_successfully_Placed/<int:order_id>", successfully_placed_order_view_create, name="order_successfully_placed"),
]