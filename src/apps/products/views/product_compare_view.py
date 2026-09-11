from django.shortcuts      import render, get_object_or_404
from apps.products.models  import Product, ProductComparison
from django.views.generic  import ListView, View
from django.urls           import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_http_methods
from django.http           import JsonResponse

class SessionMixin:

    def get_or_create_session_key(self, request):
        if not request.session.session_key:
            request.session.create()
            
        return request.session.session_key

# compare page for items. for re-usable view for count and compare listing
class CompareMixin(SessionMixin):
    # compare product count for mixin
    def get_compare_counts(self, request):
        # requesting for the user
        user = request.user
        
        # checking if the user exist
        if user.is_authenticated:
            # returns the number of comparison product exist
           return ProductComparison.objects.filter(user=user).count

        # section for user saved in the cookie
        else:
            # checking if the session exist and creating new session if not
            session_key = self.get_or_create_session_key(request)
            
            # returning filtered product that was counted
            return Product.objects.filter(
                product_comparison__session_key=session_key
            ).count()

    # filtering all compared product from anonymous users and authenticated users
    def get_comparison_products(self, request):
        # requesting for user
        user = request.user

        # checking if user is authenticated
        if user.is_authenticated:
            # returning product for user comparison
            return ProductComparison.objects.filter(user=user)
            
        # for session anonymous users
        else:
            # tries and check if there's any session for anonymous user
            session_key = self.get_or_create_session_key(request)

            # filtering product for anonymous users
            return Product.objects.filter(
                product_comparison__session_key=session_key
            )
    
# add product to comparison view set
class AddToComparisonView(CompareMixin, SessionMixin, View):
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
                    ProductComparison.objects.create(
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
            session_key = self.get_or_create_session_key(request)

            # filtering product for anonymous user
            compare_product = ProductComparison.objects.filter(
                session_key=session_key,
                product=product
            )

            # validating if compare product exist for anonymous user
            if not compare_product.exists():
                # counting compare product
                compare_count = ProductComparison.objects.filter(
                    session_key=session_key,
                ).count()

                # checking if anonymous user compare product is equal to max compare
                if compare_count < MAX_COMPARE:
                    ProductComparison.objects.create(
                        session_key=session_key,
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
class RemoveFromCompareView(CompareMixin, SessionMixin, View):
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
            session_key = self.get_or_create_session_key(request)

            # filtering product compare for session and delete it
            ProductComparison.objects.filter(
                session_key=session_key,
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
        compare_count = self.get_compare_counts(self.request)
        context['comparison_count'] = compare_count
        context['breadcrumbs'] = self.get_breadcrumbs()

        return context
    

