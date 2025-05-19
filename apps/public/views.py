from django.shortcuts import render, redirect
from apps.products.models import Category
from django.core.exceptions import PermissionDenied
from .models import OcliconTeamMembers, FrequentlyAskedQuestions
from .forms import FrequentlyAskedQuestionsForms
from django.http import JsonResponse
from django.urls import reverse

# Create your views here.

# home page view
def Home_page(request):
    context = {'show_newsletter': True, 'show_navbar_ads': True}
    return render(request, 'public/home.html', context)

# about page view
def about_page(request):
    teams = OcliconTeamMembers.objects.all()
    context = {'show_newsletter': True, 'teams': teams}
    return render(request, 'public/about.html', context)

# community page view
def comment_page(request):
    context = {}
    return render(request, 'public/comments.html', context)

def frequently_asked_question(request):
    form = FrequentlyAskedQuestionsForms()
    active_faq = FrequentlyAskedQuestions.objects.filter(active_faq=True)

    if request.method == 'POST':
        form = FrequentlyAskedQuestionsForms(request.POST)
        if form.is_valid(): #validates whether form is valid or not
            form.save() # saves the form
    else:
        form = FrequentlyAskedQuestionsForms()
    
    # breadcrumbs
    breadcrumbs = [
        ('Pages', '#/'),
        ('FAQs', request.path),
    ]
    
    context = {"breadcrumbs": breadcrumbs, "form": form, "active_faq": active_faq}
    return render(request, 'public/faq.html', context)

# renders 404 page
def page_not_found(request, exceptions):
    # renders a 404 page to the server in production mode
    return render(request, '404.html', status=404)

# customer support view
def customer_support(request):
    breadcrumbs = [
        ('Customer Support', request.path)
    ]
    return render(request, 'public/customersupport.html', {'breadcrumbs': breadcrumbs})

# blog page
def blog(request):
    breadcrumbs = [
        ('Pages', '#/'),
        ('Blog', request.path),
    ]
    return render(request, 'public/blog.html', {'breadcrumbs': breadcrumbs})

# blog details page
def blog_details(request):
    breadcrumbs = [
        ('Pages', '#/'),
        ('Blog', reverse('blog')),
        ('Blog Detail', request.path)
    ]
    return render(request, 'public/blog_details.html', {'breadcrumbs': breadcrumbs})