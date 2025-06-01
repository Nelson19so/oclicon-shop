from django.shortcuts import render, redirect
from apps.products.models import Category, Product, ProductHighlight, Badge
from django.core.exceptions import PermissionDenied
from .models import OcliconTeamMembers, FrequentlyAskedQuestions, BlogPost
from .forms import FrequentlyAskedQuestionsForms
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse

# home page view
def Home_page(request):
    computer_accessories = Product.objects.none()
    # queryset_computer_acc= request.GET.get('category_child')
    computer_category = None
    computer_category = None
    best_hot_deals = None
    best_deals_product = Product.objects.none()  
    featured_product = Product.objects.none()  

    try:
        # Get the "Computer Accessories category
        computer_category = Category.objects.prefetch_related('children').get(name='Computer Accessories')

        # Filter products marked as 'best_deal' and active
        best_deals_product = Product.objects.filter(
            is_active=True,
            product_feature__features='best_deal',
            product_feature__is_active=True
        ).select_related('product_feature')

        # best hot deals for best deals product
        best_hot_deals_badge = Badge.objects.filter(bade_type='hot').first()

        # checks if there is best hot deal
        if best_hot_deals_badge:
            best_hot_deals = (
                best_deals_product.filter(product_badge=best_hot_deals_badge)[:1]
            )

        # featured product
        featured_product = Product.objects.filter(
            is_active=True,
            product_feature__features='featured_product',
            product_feature__is_active=True
        ).select_related('product_feature')[:8]

        # Get all child categories
        child_categories = list(computer_category.children.all()[:3])

        # Filter products that belong to the child categories only
        computer_accessories = Product.objects.filter(
            is_active=True,
            category__in=child_categories,
        )

        # if queryset_computer_acc:
        #     computer_accessories = computer_accessories.filter(
        #         category__name__icontains=queryset_computer_acc
        #     )[:8]

        best_deals_product = best_deals_product[:8]

    except (Category.DoesNotExist, Product.DoesNotExist):
        pass

    # AJAX handling for computer accessories
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('products/partials/computer_accessories.html', {
            'computer_accessories': computer_accessories
        })
        return JsonResponse({'html': html})

    # AJAX handling for featured product
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('products/partials/computer_accessories.html',{
            'featured_product': featured_product
        })
        return JsonResponse({'html': html})

    context = {
        'show_newsletter': True, 
        'show_navbar_ads': True,
        'computer_accessories': computer_accessories, 
        'computer_category': computer_category,
        # 'queryset_computer_acc': queryset_computer_acc,
        'best_deals_product': best_deals_product,
        'featured_product': featured_product,
        'best_hot_deals': best_hot_deals,
        'child_categories': child_categories,
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
        if form.is_valid(): # validates whether form is valid or not
            form.save() # saves the form
    else:
        form = FrequentlyAskedQuestionsForms()
    
    # breadcrumbs
    breadcrumbs = [
        ('Pages', '#/'),
        ('FAQs', request.path),
    ]
    
    context = {
        "breadcrumbs": breadcrumbs, "form": form, "active_faq": active_faq}
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
    blogs = BlogPost.objects.all()
    
    breadcrumbs = [
        ('Pages', '#/'),
        ('Blog', request.path),
    ]
    return render(request, 'public/blog.html', {'breadcrumbs': breadcrumbs, 'blogs': blogs})

# blog details page
def blog_details(request, id):
    blog_details = BlogPost.objects.get(id=id)
    
    breadcrumbs = [
        ('Pages', '#/'),
        ('Blog', reverse('blog')),
        ('Blog Detail', request.path)
    ]

    return render(request, 'public/blog_details.html', {
        'breadcrumbs': breadcrumbs, 
        'blog_details': blog_details
    })
