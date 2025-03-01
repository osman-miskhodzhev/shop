from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from products.models import Product


class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('products:homepage')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'index.html')
