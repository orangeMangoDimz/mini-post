from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.username = 'admin'
        self.password = 'admin123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        return super().setUp()

    def test_login_user_GET(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        print("LOGIN VIEW PASSED")
    
    def test_login_user_POST_success(self):
        data = {
            'username': self.username,
            'password': self.password
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('posts'))
        print("LOGIN SUCCESS PASSED")

    def test_login_user_POST_failed(self):
        data = {
            'username': 'unknown',
            'password': 'unknown'
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        self.assertContains(response, 'Invalid username or password')
        print("LOGIN FAILURE PASSED")

    def test_logout_user_POST_success(self):
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        print("LOGOUT SUCCESS PASSED")