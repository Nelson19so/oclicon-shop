from django.test import TestCase
from apps.products.models import Brand

# test Brand model
class BrandModelTest(TestCase):
    def test_brand_models(self):
        brand = Brand.objects.create(name='testBrand')
        self.assertEqual(str(brand), 'testBrand')
    