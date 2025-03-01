from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.forms import UserRegistrationForm
from users.models import CustomUser


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {
            'first_name': 'Valerii', 'last_name': 'Pavlikov',
            'username': 'valerii', 'email': 'valerypavlikov@yandex.ru',
            'password1': '12345678pP', 'password2': '12345678pP',
        }
    
    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Регистрация')
        self.assertTemplateUsed(response, 'registration/registration.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(CustomUser.objects.filter(username=username).exists())
        
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(CustomUser.objects.filter(username=username).exists())
