from django.shortcuts import get_object_or_404
from apps.products.models import Product, Brand, Category, ProductComparison, ProductHighlight
from apps.products.forms import ReadOnlyProductSpecificationForm
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.db.models import Q
from apps.cart.models import WishlistProduct, CartItem, Cart

class SessionMixin:
    def get_or_create_session_key(self, request):
        if not request.session.session_key:
            request.session.create()
        return request.session.session_key

# product details view page
class ProductDetailView(DetailView, SessionMixin):
    model = Product
    template_name = 'products/product-details.html'
    context_object_name = 'product'

    # getting objects for getting products details
    def get_object(self, queryset=None):
        # getting category, child slug and product slug
        self.category_slug = self.kwargs.get('category_slug')
        self.child_slug = self.kwargs.get('child_slug')
        self.product_slug = self.kwargs.get('product_slug')
    
        # filtering product that inherit this category and child slug and returns 404 if None
        return get_object_or_404(
            Product,
            category__slug=self.category_slug,
            category__children__slug=self.child_slug,
            slug=self.product_slug
        )

    # breadcrumb for product details page
    def get_breadcrumbs(self):
        # getting product from get object
        product = self.get_object()

        category = Category.objects.filter(slug=self.category_slug).first()

        category_child = Category.objects.filter(
            slug=self.child_slug, parent__slug=self.category_slug
        ).last()
        
        return [
            ('Shop', reverse('shop')),
            ('Shop grid', '#/'),
            (category.name, f'/home/shop/{category.slug}/'),
            (category_child.name, f'/home/shop/{category.slug}/{category_child.slug}/'),
            (product.name, self.request.path),
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
    
    # filter for featured product
    def featured_product(self):
        # filters active featured product as well as active product
        feature_product = ProductHighlight.objects.filter(
            is_active=True, product__is_active=True
        ).order_by('?')[:3]
        return feature_product
    
    def product_accessories(self):
        product_accessories = []
        
        # filters product for product accessories
        product_accessories = Product.objects.filter(
            is_active=True,
            category__name__in=['Mobile Accessories', 'Computer Accessories']
        ).order_by('?')[:3]
        return product_accessories
    
    def check_wishlist(self, request):
        product = self.get_object()
        exist_in_wish = False
        session_key = self.get_or_create_session_key(request)
        
        try:
            if request.user.is_authenticated:
                if WishlistProduct.objects.filter(user=request.user, product=product).exists():
                    exist_in_wish = True
            else:
                if WishlistProduct.objects.filter(session_key=session_key, product=product).exists():
                    exist_in_wish = True
        except WishlistProduct.DoesNotExist:
            pass
        
        return exist_in_wish
    
    def check_cart(self, request):
        product = self.get_object()
        cart = None
        cart_exist = False
        session_key = self.get_or_create_session_key(request)

        try:
            if request.user.is_authenticated:
                cart = Cart.objects.get(user=request.user)
                if cart and CartItem.objects.filter(cart=cart, product=product).exists():
                    cart_exist = True
            else:
                cart = Cart.objects.get(session_key=session_key)
                if cart and CartItem.objects.filter(cart=cart, product=product).exists():
                    cart_exist = True
        except Cart.DoesNotExist or CartItem.DoesNotExist:
            pass

        return cart_exist

    def check_compare(self, request):
        product = self.get_object()
        compare_exist = False
        session_key = self.get_or_create_session_key(request)

        try:
            if request.user.is_authenticated:
                if ProductComparison.objects.filter(user=request.user, product=product).exists():
                    compare_exist = True
            else:
                if ProductComparison.objects.filter(session_key=session_key, product=product).exists():
                    compare_exist = True
        except ProductComparison.DoesNotExist:
            pass

        return compare_exist
            
    # getting additional information for product to use in the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object() # getting returned object to query data
        context['variant'] = product.variant.first()
        context['breadcrumbs'] = self.get_breadcrumbs()
        context['badges'] = product.product_badge.first()
        context['form'] = self.get_product_specification()
        context['related_products'] = self.get_related_product()
        context['feature_products'] = self.featured_product()
        context['product_accessories'] = self.product_accessories()
        context['exist_in_wish'] = self.check_wishlist(self.request)
        context['cart_exist'] = self.check_cart(self.request)
        context['compare_exist'] = self.check_compare(self.request)
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
        self.brand = None
        # query for searching for product
        query = self.request.GET.get('q')

        # getting url slug for category, child category and brand
        category_slug = self.kwargs.get('category_slug')
        child_slug = self.kwargs.get('child_slug')
        brand_slug = self.kwargs.get('brand_slug')

        # filters product under the category
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug, parent=None)
            queryset = queryset.filter(category=self.category)

        # filter product under the category and child category
        if child_slug:
            self.child_category = get_object_or_404(Category, slug=child_slug, parent__slug=category_slug)
            queryset = queryset.filter(category=self.child_category)

        # filter category under the brand
        if brand_slug:
            self.brand = get_object_or_404(Brand, slug=brand_slug)
            queryset = queryset.filter(brand=self.brand)

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

        if self.brand:
            url = f'/shop/{self.brand.slug}/'
            # if self.child_category:
            #     url += f'{self.child_category.slug}/'
            # url += f'{self.brand.slug}/'
            breadcrumbs.append((self.brand.name, url))

        return breadcrumbs

    # for showing user active filters in shop page
    def show_category(self):
        # filters category slug
        category_slug = self.kwargs.get('category_slug')

        # checks if category exist
        if category_slug:
            return Category.objects.get(slug=category_slug)
        return None
    
    # def product_wishlist_cart_compare_exist(self, request):
    #     pass

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
        context['category_name'] = self.show_category()
        context['product_count'] = product.count()
        context['query'] = self.request.GET.get('q', '')
        return context
