from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Add Debug Toolbar URLs in debug mode
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]