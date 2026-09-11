import requests
from django.shortcuts import render, redirect
from .models import TempPayment
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_GET
from django.views import View
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
from apps.orders.models import Order

class StartOrderPayment(View):
    @method_decorator(require_POST)
    def post(self, request):
        user = request.user

        reference = f"TXN{user.id}{timezone.now().strftime('%Y%m%d%H%M%S')}"

        try:
            
            order = Order.objects.filter(user=user)
            order_total_amount = order.total_amount

            total_amount = order_total_amount
            TempPayment.objects.create(user=user, reference=reference, amount=total_amount)

            headers = {
                "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "email": user.email,
                "amount": int(total_amount * 100),  # in kobo
                "reference": reference,
                "callback_url": "http://localhost:8000/payments/verify/",
            }
            
            res = requests.post("https://api.paystack.co/transaction/initialize", json=data, headers=headers)
            auth_url = res.json()['data']['authorization_url']

            return redirect(auth_url)
            
        except Order.DoesNotExist:
            return redirect('home')

class VerifyPaymentOrderView(View):
    @method_decorator(require_GET)
    def get(self, request):
        reference = request.Get.get('reference')

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }

        url = f"https://api.paystack.co/transaction/verify/{reference}"
        response = requests.get(url, headers=headers)
        result = response.json()

        if result['data']['status'] == 'success':
            pass
            # logics goes here but since we are still working on it, we will use pass method
            # this method processes wen the payment is successful

            return HttpResponse("✅ Payment successful and order created.")

        return HttpResponse("❌ Payment failed.")
