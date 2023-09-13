from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'example.email@example.comm'
        password = 'testPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user normalized"""
        email = "test@GMAIL.COM"
        user = get_user_model().objects.create_user(
            email=email,
            password='test123'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with invalid email error raises"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='test123'
            )

    def test_create_new_super_user(self):
        """Test creating super user"""
        superuser = get_user_model().objects.create_superuser(
            email='super@gmail.com',
            password="superpass"
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)