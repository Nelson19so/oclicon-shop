from django.urls import path
from .views import ProductDetailView, FilteredProductListView, ComparisonPageView, AddToComparisonView

urlpatterns = [
    # shop url conf
    path('shop/', FilteredProductListView.as_view(), name="shop"),
    # shop by category
    path('shop/<slug:category_slug>/', FilteredProductListView.as_view(), name='shop_category'),  
    # shop by child category
    path('shop/<slug:category_slug>/<slug:child_slug>/', FilteredProductListView.as_view(), name='shop_child_category'),  
    # shop by child + brand
    path('shop/brand/<slug:brand_slug>/', FilteredProductListView.as_view(), name='shop_brand'),  
    # product details
    path('shop/product-details/<slug:category_slug>/<slug:child_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='product_details'), 

    # comparison url conf
    path('compare/', ComparisonPageView.as_view(), name='compare'),
    path('compare/add/<int:product_id>/', AddToComparisonView.as_view(), name='add_compare'),
    path('compare/remove/<int:product_id>/', ComparisonPageView.as_view(), name='remove_compare'),
]


