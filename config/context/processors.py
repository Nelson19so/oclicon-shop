from apps.products.models import Category, Product, Ad, ProductHighlight

# context processor for category list for navbar
def navbar_categories_list(request):
    # filters all category and it related children
    categories = Category.objects.prefetch_related('children').filter(parent=None)
    # returns the category for use.
    return {"categories": categories}


# breadcrumbs
# not yet in settings.py context processor
def breadcrumbs_processor(request):
    return {
        'breadcrumbs': []  # default fallback
    }
