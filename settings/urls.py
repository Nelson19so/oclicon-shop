from django.contrib import admin
from django.conf import settings
# from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),    
    path('accounts/', include('allauth.urls')),  # for allauth URLs

    # public pages
    path('', include('apps.public.urls')),
    path('home/', include('apps.public.urls')),
]

# Add Debug Toolbar URLs in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     import debug_toolbar
    # urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]