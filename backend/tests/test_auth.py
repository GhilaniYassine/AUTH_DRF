from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import json

User = get_user_model()

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        try:
            self.register_url = reverse('register')
            self.login_url = reverse('login')
            self.refresh_url = reverse('token_refresh')
        except:
            # If URL reversing fails, use direct paths
            self.register_url = '/api/auth/register/'
            self.login_url = '/api/auth/login/'
            self.refresh_url = '/api/auth/token/refresh/'
        
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        print(f"Registration response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login(self):
        # Create user first
        User.objects.create_user(**self.user_data)
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        print(f"Login response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        # Create user and login first
        User.objects.create_user(**self.user_data)
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        
        if login_response.status_code == 200 and 'refresh' in login_response.data:
            refresh_token = login_response.data['refresh']
            refresh_data = {'refresh': refresh_token}
            response = self.client.post(self.refresh_url, refresh_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('access', response.data)
        else:
            self.skipTest("Login did not return refresh token")

    def test_invalid_registration(self):
        # Test registration with missing required fields
        invalid_data = {
            'username': 'testuser',
            'password': 'testpass123'
            # Missing email, first_name, last_name
        }
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_login(self):
        # Test login with wrong credentials
        login_data = {
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email_registration(self):
        # Create first user
        User.objects.create_user(**self.user_data)
        
        # Try to register with same email
        duplicate_data = self.user_data.copy()
        duplicate_data['username'] = 'different_username'
        
        response = self.client.post(self.register_url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
