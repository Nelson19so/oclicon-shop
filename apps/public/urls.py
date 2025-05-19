from django.urls import path
from .views import (
    page_not_found, 
    Home_page, 
    comment_page, 
    frequently_asked_question, 
    about_page, customer_support, 
    blog, 
    blog_details
)
from django.conf.urls import handler404

urlpatterns = [
    path('', Home_page, name="home"),
    path('about/', about_page, name='about' ),
    path('comment/', comment_page, name="comments"),
    path('faqs/', frequently_asked_question, name='faqs'),
    path('customersupport/', customer_support, name="customersupport"),
    path('blog/', blog, name='blog'),
    path('blog/blog_details/', blog_details, name='blog_details'),
]

handler404 = page_not_found