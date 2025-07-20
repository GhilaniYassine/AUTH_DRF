from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class UserModelTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_creation(self):
        """Test that we can create a user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_user_str_method(self):
        """Test the user string representation"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), user.email)

    def test_user_required_fields(self):
        """Test that required fields are properly set"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.email)
        self.assertTrue(user.username)

    def test_user_email_unique(self):
        """Test that email is unique"""
        User.objects.create_user(**self.user_data)
        
        # Try to create another user with same email
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                email='test@example.com',  # Same email
                password='testpass123',
                first_name='Test2',
                last_name='User2'
            )

    def test_username_field_is_email(self):
        """Test that email is used as the username field"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(User.USERNAME_FIELD, 'email')
        self.assertEqual(user.get_username(), user.email)
