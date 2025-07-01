from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    # admin url
    path('admin/', admin.site.urls),    

    # google authentication
    path('accounts/', include('allauth.urls')),  # for allauth URLs

    # User account
    path('home/user_account/', include('apps.accounts.urls')),

    # public url conf
    path('', include('apps.public.urls')),
    path('home/', include('apps.public.urls')),

    # product url conf
    path('home/', include('apps.products.urls')),

    # order url conf
    path('home/user_account/', include('apps.orders.urls')),

    # cart url conf
    path('home/', include('apps.cart.urls')),

    # PayStack payment gateway url configuration
    path('home/payment', include('apps.payments.urls'))
]

# Add Debug Toolbar URLs in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # import debug_toolbar
    # urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]