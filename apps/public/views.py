from django.shortcuts import render

# Create your views here.

def Home_page(request):
  return render(request, 'dashboard/home.html', {'show_extra': True})

def shop_page(request):
  return render(request, 'shop/shop.html', {'show_extra': False})