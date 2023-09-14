from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# allows us to make test requests to our API and check the response
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

user_payload = {
    'email': 'test@gmail.com',
    'password': '12346',
    'username': 'test'
}


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""

        res = self.client.post(CREATE_USER_URL, user_payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(user_payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """Test creating exist user fails"""
        create_user(**user_payload)

        res = self.client.post(CREATE_USER_URL, user_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = user_payload
        payload['password'] = 'pw'

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        is_user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(is_user_exist)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        create_user(**user_payload)

        res = self.client.post(TOKEN_URL, user_payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_with_invalid_credential(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(**user_payload)
        payload = {
            'email': 'email@gmail.com',
            'password': 'wrong'
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_user(self):
        """Test that creating token without user fails"""

        res = self.client.post(TOKEN_URL, user_payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_password(self):
        """Test that creating token without password fails"""
        payload = user_payload.copy()
        create_user(**user_payload)

        payload.pop('password')

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_email(self):
        """Test that creating token without password fails"""
        payload = user_payload.copy()
        create_user(**user_payload)

        payload.pop('email')

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
