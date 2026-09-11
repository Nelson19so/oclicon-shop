from apps.products.models import Category, Product, Ad, ProductHighlight

# context processor for category list for navbar
def navbar_categories_list(request):
    # filters all category and it related children
    categories = Category.objects.prefetch_related('children').filter(parent=None)

    # Filters hot related product
    hot_products = Product.objects.filter(
        is_active=True, product_badge__bade_type='hot'
    ).prefetch_related('variant',)

    for category in categories:
        category.hot_products = [p for p in hot_products if p.category == category]
    
    # returns the category for use.
    return {"categories": categories}

# breadcrumbs
# not yet in settings.py context processor
def breadcrumbs_processor(request):
    return {
        'breadcrumbs': []  # default fallback
    }
