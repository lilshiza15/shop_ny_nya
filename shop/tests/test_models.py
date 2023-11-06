from django.test import TestCase

from shop.models import Category,Product

class TestCategoriesModel(TestCase):
    def setUp(self) -> None:
        self.data1 = Category.objects.create(name='title',slug='title',img='categories/laptop.png')
    
    def test_category_model_entry(self):
        data = self.data1
        self.assertTrue(isinstance(data,Category))