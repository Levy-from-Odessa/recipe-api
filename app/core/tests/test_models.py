from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="test@gmail.com", password="testpass"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'example.email@example.comm'
        password = 'testPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username="test",
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user normalized"""
        email = "test@GMAIL.COM"
        user = get_user_model().objects.create_user(
            email=email,
            password='test123',
            username="test"
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with invalid email error raises"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='test123',
                username="test"
            )

    def test_create_new_super_user(self):
        """Test creating super user"""
        superuser = get_user_model().objects.create_superuser(
            email='super@gmail.com',
            password="superpass",
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
