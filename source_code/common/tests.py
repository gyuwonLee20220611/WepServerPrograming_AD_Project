from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class SignupViewTests(TestCase):
    def test_signup_creates_user_and_redirects_to_index(self):
        response = self.client.post(reverse('common:signup'), {
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password1': 'strong-password-123',
            'password2': 'strong-password-123',
        })

        self.assertRedirects(response, reverse('index'))
        self.assertTrue(User.objects.filter(username='new_user').exists())
