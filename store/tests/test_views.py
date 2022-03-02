from unittest import skip

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import all_products


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='django', created_by_id=1,
                               slug='django', price='20.00', image='django')
     
    def test_url_allowed_hosts(self):
        """test allowed hosts
        """
        response =self.c.get('/')
        self.assertEqual(response.status_code, 200)    
    
    def test_product_detail_url(self):
        response = self.c.get(reverse('store:product_detail', args=['django']))
        self.assertEqual(response.status_code, 200)
        
    def test_category_detail_url(self):
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)
        
    def test_homepage_html(self):
        request =HttpRequest()
        response = all_products(request)
        html = response.content.decode('utf8')
        print(html)
        self.assertIn('<title>BookStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_fuction(self):
        request = self.factory.get('/item/django')
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>BookStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)