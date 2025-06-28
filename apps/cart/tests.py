from django.test import TestCase, Client
from .models import Cart, CartItem, WishlistProduct
from django.urls import reverse
from apps.products.models import Product, Category, Brand
from django.contrib.auth import get_user_model

User = get_user_model()

class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            Name='testUser', email='testUser@gmail.com', password='12wsx3edc.'
        )
        self.brand = Brand.objects.create(name='testProductBrand')
        self.category = Category.objects.create(name='testProductCategory')
        self.product = Product.objects.create(
            name='testProduct',
            brand=self.brand,
            category=self.category,
            base_price='300',
            discount_price='400',
            description='testProductDescription',
            is_active=True
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=1
        )

    def test_update_cart_quantity_authenticated(self):
        self.client.login(email='testUser@gmail.com', password='12wsx3edc.')
        response = self.client.post(reverse('cart_update'), {'item_ids': [str(self.cart.id)]})
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 3)
        self.assertEqual(response.status_code, 302)
