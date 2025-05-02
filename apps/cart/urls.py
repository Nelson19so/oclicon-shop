from django.urls import path
from .views import CreateCartItem, RemoveItemFromCart, WishListProductCreate, RemoveItemFromWishlist, CartItemListView, update_cart_quantities, wish_list_view

urlpatterns = [
    path('cart/', CartItemListView.as_view(), name='cart_list'),
    path('cart/add/<slug:product_slug>/', CreateCartItem.as_view(), name="add_to_cart"),
    path('cart/remove/<int:cart_id>/', RemoveItemFromCart.as_view(), name="remove_from_cart"),
    path('cart/update/', update_cart_quantities, name="cart_update"),

    # wish list url configuration
    path('wishlist/', wish_list_view, name='wishlist'),
    path('wishlist/add/<slug:product_slug>/', WishListProductCreate.as_view(), name="add_to_wishlist"),
    path('wishlist/remove/<int:cart_id>/', RemoveItemFromWishlist.as_view(), name="remove_from_wishlist")
]