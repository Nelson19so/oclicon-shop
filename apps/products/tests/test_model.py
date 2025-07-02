from django.test import TestCase
from apps.products.models import Brand, Category

# test category model
class ProductsModelTest(TestCase):
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
