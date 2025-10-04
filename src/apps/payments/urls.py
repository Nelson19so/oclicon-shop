from django.urls import path
from .views import StartOrderPayment, VerifyPaymentOrderView

urlpatterns = [
    path('start/', StartOrderPayment.as_view(), name='paystack-order-start'),
    path('verify/', VerifyPaymentOrderView.as_view(), name='paystack-order-verify'),
]