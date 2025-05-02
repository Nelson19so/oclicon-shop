from django.urls import path
from .views import page_not_found, Home_page, comment_page
from django.conf.urls import handler404

urlpatterns = [
    path('', Home_page, name="home"),
    path('comment/', comment_page, name="comments"),
]

handler404 = page_not_found