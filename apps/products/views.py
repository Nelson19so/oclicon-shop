from django.shortcuts import render, get_object_or_404
from .models import Product, ProductVariant, ProductImage, Brand, Category, ProductComparison
from django.views.generic import ListView, DetailView
from django.db.models.functions import Random
from django.contrib.sessions.models import Session
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
import random

# Create your views here.

# product details
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product-details.html'
    context_object_name = 'product'

    # getting objects for getting products details
    def get_object(self, queryset=None):
        # getting category anc child slug for product
        category_slug = self.kwargs.get('category_slug')
        child_slug = self.kwargs.get('child_slug')
        product_slug = self.kwargs.get('product_slug')
    
        # filtering related url for getting product that matches the queryset
        return get_object_or_404(
            Product,
            category__slug=category_slug,
            category__children__parent__slug=child_slug,
            slug=product_slug
        )

    # getting additional information for product
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object() # getting returned object to query data

        context['main_image'] = product.variant.first().images.first() if product.variant.exists() else None
        context['all_images'] = product.variant.first().images.all() if product.variant.exists() else []
        context['colors'] = set(v.color for v in product.variant.all() if v.color)
        context['specifications'] = set(v.product_specification for v in product.variant.all() if v.product_specification)

        return context

# shop page for items --------
# All random product
class RandomProductListView(ListView):
    model = Product
    template_name = 'pages/shop/shop.html'
    context_object_name = 'products'
    paginate_by = 24

    def get_queryset(self):
        # filtering active product
        return Product.objects.filter(
            is_active=True
        ).order_by(Random()).prefetch_related( # getting related data
            'variants__images',
            'brand',
            'category'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all() # getting all categories
        return context

# filtering for all kinds of product category, category child, brand and all product
class FilteredProductListView(ListView):
    model = Product
    template_name = 'pages/shop/shop.html'
    context_object_name = 'products'
    paginate_by = 24

    def get_queryset(self):
        # listing all product for listing in the template
        queryset = Product.objects.filter(is_active=True)
        category_slug = self.kwargs.get('category_slug')
        child_slug = self.kwargs.get('child_slug')
        brand_slug = self.kwargs.get('brand_slug')

        # filtering for product under this category in the slug
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug, parent=None)
            queryset = queryset.filter(category=category)

        # filtering for product under this child category in the slug
        if child_slug:
            child_category = get_object_or_404(Category, slug=child_slug, parent__slug=category_slug)
            queryset = queryset.filter(category=child_category)

        # filtering for product under this brand in the slug
        if brand_slug:
            brand = get_object_or_404(Brand, slug=brand_slug)
            queryset = queryset.filter(brand=brand)

        # getting related product variants from the product
        return queryset.prefetch_related(
            'variants__images',
            'brand',
            'category'
        )

    # additional context being passed for rendering product
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category_slug'] = self.kwargs.get('category_slug')
        context['child_slug'] = self.kwargs.get('child_slug')
        context['brand_slug'] = self.kwargs.get('brand_slug')
        return context

# compare page for items. for re-usable view for count and compare listing
class CompareMixin:
    def get_compare_counts(self, request):
        user = request.user
        
        if user.is_authenticated:
           return ProductComparison.objects.filter(user=user).count

        # section for user saved in the cookie
        else:
            if not request.session.session_key:
                return 0
            
            return Product.objects.filter(
                productcomparison__session_id=request.session.session_key
            ).count()

    # filtering all compared product from session and for user
    def get_comparison_products(self, request):
        user = request.user

        # for user
        if user.is_authenticated:
            return ProductComparison.objects.filter(user=user)
            
        # for session
        else:
            if not request.session.session_key:
                return Product.objects.none()
        
            return Product.objects.filter(
                productcomparison__session_id=request.session.session_key
            ).prefetch_related('variant', 'category', 'badge', 'images') # filtering related
    
class AddToComparisonView(CompareMixin, View):
    @method_decorator(require_http_methods([require_POST])) # allowing only post method for this view
    def post(self, request, *args, **kwargs):
        user = request.user
        MAX_COMPARE = 5 # max compared product to add

        # for logged in users --
        if user.is_authenticated:
            product = get_object_or_404(Product, id=kwargs['product_id'])

            compare_product = ProductComparison.objects.filter(
                user=user,
                product=product
            )

            # validating compare product
            if not compare_product:
                if compare_product.count() <= MAX_COMPARE:
                    ProductComparison.objects.get_or_create(
                        user=user,
                        product=product
                    )
                else: # passes json
                    return JsonResponse({
                        'status': 'failed',
                        'error': "You can't add more product to compare"
                    })
        # session for user
        else:
            if not request.session.session_key:
                request.session.create()
            
            product = get_object_or_404(Product, id=kwargs['product_id'])
            
            compare_product = ProductComparison.objects.filter(
                session_id=request.session.session_key,
                Product=product
            )

            # validating compare product
            if not compare_product:
                ProductComparison.objects.get_or_create(
                    session_id=request.session.session_key,
                    product=product
                )

        return JsonResponse({
            'status': 'success',
            'count': self.get_compare_counts(request)
        })
    
# for removing compare product for user and session cookies
class RemoveFromCompareView(CompareMixin, View):
    @method_decorator(require_http_methods([require_POST])) # allowing only post request
    def post(self, request, *args, **kwargs):
        user = request.user

        # checking if user is authenticated
        if user.is_authenticated:
            ProductComparison.objects.filter(
                user=user,
                product_id=kwargs['product_id'], 
            )

        # for session anonymous users
        else:
            if not request.session.session_key:
                request.session.create()
                session_id = request.session
            
            # filtering product compare for session
            ProductComparison.objects.filter(
                session_id=session_id,
                product_id=kwargs['product_id']
            ).delete()

        # returning a json response to the user
        return JsonResponse({
            'status': 'success',
            'count': self.get_compare_counts(request)
        })
    
# compare product list view for listing all compare product
class ComparisonPageView(CompareMixin, ListView):
    template_name = 'pages/compare.html'
    context_object_name = 'comparison'

    # query set data to use the compareMixin class for querying all compare product
    def get_queryset(self):
        return self.get_comparison_products(self.request)
    
    # getting the compare counts for displaying in the UI
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comparison_count'] = self.get_compare_counts(self.request)
        return context
