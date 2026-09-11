from django.test import TestCase, Client
from apps.products.models import Brand, Category
from django.contrib.auth import get_user_model

User = get_user_model()

# testing all product model for product app
class ProductsModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='tesUser', email='testemail@gmail.com', password='testpassword_12.'
        )
        self.logged_in = self.client.login(
            email='testemail@gmail.com', password='testpassword_12.'
        )

    def test_products_models(self):
        brand = Brand.objects.create(name='testBrand')
        category = Category.objects.create(
            name='testCategory'
        )
        children = Category.objects.create(
            name='testCategoryChild',
            parent=category
        )
        self.assertEqual(str(brand), 'testBrand')
        self.assertEqual(str(category), 'testCategory')
        self.assertEqual(str(children), 'testCategoryChild')
