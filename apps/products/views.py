from django.shortcuts import render, get_object_or_404
from .models import Product, ProductVariant, ProductImage, Brand, Category, ProductComparison, Badge
from .forms import ReadOnlyProductSpecificationForm
from django.views.generic import ListView, DetailView, View, TemplateView
from django.db.models.functions import Random
from django.contrib.sessions.models import Session
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.urls import reverse
from django.db.models import Q
import random
from django.core.exceptions import ObjectDoesNotExist

# product details view page
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product-details.html'
    context_object_name = 'product'

    # getting objects for getting products details
    def get_object(self, queryset=None):
        # getting category, child slug and product slug
        category_slug = self.kwargs.get('category_slug')
        child_slug = self.kwargs.get('child_slug')
        product_slug = self.kwargs.get('product_slug')
    
        # filtering product that inherit this category and child slug and returns 404 if None
        return get_object_or_404(
            Product,
            category__slug=category_slug,
            category__children__slug=child_slug,
            slug=product_slug
        )

    # breadcrumb for product details page
    def get_breadcrumbs(self):
        # getting product from get object
        product = self.get_object()
        return [
            ('Shop', reverse('shop')),
            ('Shop grid', '#/'),
            # (product.category.name, 'll'),
            # ( product.category_child.name,  product.category_child.slug),
            (product.brand, self.request.path),
        ]

    # filter related product
    def get_related_product(self):
        # getting the product details visited
        product = self.get_object()
        # getting category slug
        category = self.kwargs.get('child_slug')
        # filtering with this information and exclude this product from the filtering
        related_product = Product.objects.filter(
            category__slug=category
        ).order_by('?').exclude(id=product.id)[:3]
        return related_product
    
    # product specification
    def get_product_specification(self):
        # getting the product visited
        product = self.get_object()
        # filtering the first product specification
        specification = product.specification.first()
        return ReadOnlyProductSpecificationForm(instance=specification)
    
    # getting additional information for product to use in the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object() # getting returned object to query data
        context['variant'] = product.variant.first()
        context['breadcrumbs'] = self.get_breadcrumbs()
        context['badges'] = product.product_badge.first()
        context['form'] = self.get_product_specification()
        context['related_products'] = self.get_related_product()
        return context

# shop page for filtering and searching all kinds of product that exist in shop
class FilteredProductListView(ListView):
    model = Product
    template_name = 'products/shop.html'
    context_object_name = 'products'
    paginate_by = 24

    # query set for listing many product
    def get_queryset(self):
        # filtering active product
        queryset = Product.objects.filter(is_active=True)
        # setting category, child category, brand to None to be able to filter all product
        self.category = None
        self.child_category = None
        # self.brand = None
        # query for searching for product
        query = self.request.GET.get('q')

        # getting url slug for category, child category and brand
        category_slug = self.kwargs.get('category_slug')
        child_slug = self.kwargs.get('child_slug')
        # brand_slug = self.kwargs.get('brand_slug')

        # filters product under the category
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug, parent=None)
            queryset = queryset.filter(category=self.category)

        # filter product under the category and child category
        if child_slug:
            self.child_category = get_object_or_404(Category, slug=child_slug, parent__slug=category_slug)
            queryset = queryset.filter(category=self.child_category)

        # filter category under the brand
        # if brand_slug:
        #     self.brand = get_object_or_404(Brand, slug=brand_slug)
        #     queryset = queryset.filter(brand=self.brand)

        # checks if theres any item in search
        if query:
            # this query filters product based on user search
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

        # orders product queryset randomly
        queryset = queryset.order_by('?')

        # returns the product queryset and it related items
        return queryset.prefetch_related(
            'brand', 
            'category',
            'images',
            'product_badge'
        )

    # builds breadcrumb for product list
    def get_breadcrumbs(self):
        breadcrumbs = [('Shop', reverse('shop'))]

        if self.category:
            breadcrumbs.append((self.category.name, f'/home/shop/{self.category.slug}/'))

        # breadcrumb if theres is category and child slug
        if self.child_category:
            breadcrumbs.append((self.child_category.name, f'/home/shop/{self.category.slug}/{self.child_category.slug}/'))

        # if self.brand:
        #     url = f'/shop/{self.category.slug}/'
        #     if self.child_category:
        #         url += f'{self.child_category.slug}/'
        #     url += f'{self.brand.slug}/'
        #     breadcrumbs.append((self.brand.name, url))

        return breadcrumbs

    # additional context being passed for rendering product and it items to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_queryset()
        context['products'] = product
        context['categories'] = Category.objects.all()
        context['category_slug'] = self.kwargs.get('category_slug')
        context['child_slug'] = self.kwargs.get('child_slug')
        context['brand_slug'] = self.kwargs.get('brand_slug')
        context['breadcrumbs'] = self.get_breadcrumbs()
        context['product_count'] = product.count()
        context['query'] = self.request.GET.get('q', '')
        return context

# compare page for items. for re-usable view for count and compare listing
class CompareMixin:
    # compare product count for mixin
    def get_compare_counts(self, request):
        # requesting for the user
        user = request.user

        # requesting for anonymous user session
        session_key = request.session.session_key
        
        # checking if the user exist
        if user.is_authenticated:
            # returns the number of comparison product exist
           return ProductComparison.objects.filter(user=user).count

        # section for user saved in the cookie
        else:
            # checking if the session exist and creating new session if not
            if not request.session.session_key:
                request.session.create()
            
            # getting requested session
            session = Session.objects.filter(session_key=session_key)
            
            # returning filtered product that was counted
            return Product.objects.filter(
                product_comparison__session_id=session
            ).count()

    # filtering all compared product from anonymous users and authenticated users
    def get_comparison_products(self, request):
        # requesting for user
        user = request.user

        # requesting session key for anonymous user 
        session_key = request.session.session_key

        # checking if user is authenticated
        if user.is_authenticated:
            # returning product for user comparison
            return ProductComparison.objects.filter(user=user)
            
        # for session anonymous users
        else:
            # tries and check if there's any session for anonymous user
            try:
                session = Session.objects.get(session_key=session_key)
            except ObjectDoesNotExist:
                return Product.objects.none()
        
            # filtering product for anonymous users
            return Product.objects.filter(
                product_comparison__session_id=session
            )
    
# add product to comparison view set
class AddToComparisonView(CompareMixin, View):
    # Only post request can trigger what happens here
    require_http_methods([require_POST])
    def post(self, request, *args, **kwargs):
        # requesting for the authenticated user
        user = request.user
        # max number of compare product user can add
        MAX_COMPARE = 5 

        # filtering product to add to compare
        product = get_object_or_404(Product, id=kwargs['product_id'])

        # for authenticated users
        if user.is_authenticated:
            # filtering product for user
            compare_product = ProductComparison.objects.filter(
                user=user,
                product=product
            )

            # validating if compare product exist
            if not compare_product.exists():
                # counting compare product
                compare_count = ProductComparison.objects.filter(
                    user=user,
                ).count()

                # making sure compare product is less than max compare
                if compare_count < MAX_COMPARE:
                    ProductComparison.objects.get_or_create(
                        user=user,
                        product=product
                    )
                
                # sending user json message if the product is up to max limit
                else:
                    return JsonResponse({
                        'status': 'failed',
                        'error': "You can't add more product to compare"
                    })

        # session for user
        else:
            # creating new session if user has no session
            if not request.session.session_key:
                request.session.create()

            # requesting for session
            session_id = request.session.session_key
            # getting session
            session = Session.objects.get(session_key=session_id)

            # filtering product for anonymous user
            compare_product = ProductComparison.objects.filter(
                session_id=session,
                product=product
            )

            # validating if compare product exist for anonymous user
            if not compare_product.exists():
                # counting compare product
                compare_count = ProductComparison.objects.filter(
                    session_id=session,
                ).count()

                # checking if anonymous user compare product is equal to max compare
                if compare_count < MAX_COMPARE:
                    ProductComparison.objects.get_or_create(
                        session_id=session,
                        product=product
                    )

                # sending a json message if max anonymous user cant add more product to compare 
                else:
                    return JsonResponse({
                        'status': 'failed',
                        'error': "You can't add more product to compare"
                    })
        
        # getting count from mixin
        compare_count =  self.get_compare_counts(request)
        
        # sending user json message if the process went successfully
        return JsonResponse({
            'status': 'success',
            'count': compare_count
        })

# removing compare product for user and session cookies
class RemoveFromCompareView(CompareMixin, View):
    @method_decorator([require_POST]) # allowing only post request
    def post(self, request, *args, **kwargs):
        # requesting for authenticated users
        user = request.user

        # checking if user is authenticated
        if user.is_authenticated:
            # filtering product nad it ID and delete it
            ProductComparison.objects.filter(
                user=user,
                product_id=kwargs['product_id'],
            ).delete()

        # for session anonymous users
        else:
            # checking for if session and creating if session doesn't exist
            if not request.session.session_key:
                request.session.create()
            
            # requesting for session
            session_key = request.session.session_key
            # getting session
            session = Session.objects.get(session_key=session_key)

            # filtering product compare for session and delete it
            ProductComparison.objects.filter(
                session_id=session,
                product_id=kwargs['product_id']
            ).delete()

        # count the compare to manually update the compare
        compare_count = self.get_compare_counts()

        # return success json response if the process went well
        return JsonResponse({
            'status': 'success',
            'count': compare_count,
        })

# compare product list page view for listing all compare product
class ComparisonPageView(CompareMixin, ListView):
    template_name = 'products/compare.html'
    context_object_name = 'comparisons'

    # query set data to use the compareMixin class for querying all compare product
    def get_queryset(self):
        # this uses the compare mixin to re-use user list for auth users and anon... users
        return self.get_comparison_products(self.request)
    
    # building breadcrumb for compare product list
    def get_breadcrumbs(self):
        breadcrumbs = [
            ('Shop', reverse('shop')),
            ('Compare', self.request.path),
        ]
        # returns product
        return breadcrumbs
    
    # context for using additional queryset in the html template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # compare_count = self.get_compare_counts(self.request)
        # context['comparison_count'] = compare_count
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context
    

