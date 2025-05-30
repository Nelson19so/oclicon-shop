from django.shortcuts import render, redirect
from apps.products.models import Category, Product, ProductHighlight, Badge
from django.core.exceptions import PermissionDenied
from .models import OcliconTeamMembers, FrequentlyAskedQuestions
from .forms import FrequentlyAskedQuestionsForms
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q

# Create your views here.

# home page view
def Home_page(request):
    computer_accessories = Product.objects.none()  
    queryset_computer_acc= request.GET.get('q', '')
    computer_category = None

    try:
        # Get the "Computer Accessories category
        computer_category = Category.objects.prefetch_related('children').get(name='Computer Accessories')

        # Filter products marked as 'best_deal' and active
        best_deals_product = Product.objects.filter(
            product_feature__features='best_deal',
            product_feature__is_active=True
        ).select_related('product_feature')

        best_deals_product[:8]

        # best hot deals for best deals product
        best_hot_deals_badge = Badge.objects.filter(bade_type='hot').first()

        # checks if there is best hot deal
        if best_hot_deals_badge:
            best_hot_deals = (
                best_deals_product.filter(product_badge=best_hot_deals_badge)[:1]
            )

        # featured product
        featured_product = Product.objects.filter(
            product_feature__features='featured_product',
            product_feature__is_active=True
        ).select_related('product_feature')[:8]

        # Get all child categories
        child_categories = computer_category.children.all()

        # Filter products that belong to the child categories only
        computer_accessories = Product.objects.filter(category__in=child_categories)[:8]

        if queryset_computer_acc:
            computer_accessories = computer_accessories.filter(
                Q(category__name__icontains=queryset_computer_acc)[:8]
            )

    except (Category.DoesNotExist, Product.DoesNotExist):
        pass

    context = {
        'show_newsletter': True, 
        'show_navbar_ads': True,
        'computer_accessories': computer_accessories, 
        'computer_category': computer_category,
        'queryset_computer_acc': queryset_computer_acc,
        'best_deals_product': best_deals_product,
        'featured_product': featured_product,
        'best_hot_deals': best_hot_deals
    }
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