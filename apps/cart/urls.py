from django.urls import path
from .views.cart_view import CreateCartItem, RemoveItemFromCart, CartItemListView, update_cart_quantities
from .views.wishlist_view import WishListProductCreate, RemoveItemFromWishlist, wish_list_view

urlpatterns = [
    path('cart/', CartItemListView.as_view(), name='cart_list'),
    path('cart/add/<int:product_id>/', CreateCartItem.as_view(), name="add_to_cart"),
    path('cart/remove/<int:cart_id>/', RemoveItemFromCart.as_view(), name="remove_from_cart"),
    path('cart/update/', update_cart_quantities, name="cart_update"),

    # wish list url configuration
    path('wishlist/', wish_list_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', WishListProductCreate.as_view(), name="add_to_wishlist"),
    path('wishlist/remove/<int:product_id>/', RemoveItemFromWishlist.as_view(), name="remove_from_wishlist")
]
