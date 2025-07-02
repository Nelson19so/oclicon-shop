from django.test import TestCase
from apps.products.models import Brand, Category

# test Brand model
class ProductModelTest(TestCase):
    def product_model_test(self):
        brand = Brand.objects.create(name='testBrand')
        category = Category.objects.create(
            name='testCategory'
        )
        children = Category.objects.create(
            name='testCategoryChild',
            parent=category
        )
        self.assertEqual(str(category), 'testCategory')
        self.assertEqual(str(children), 'testCategoryChild')
        self.assertEqual(str(brand), 'testBrand')

        