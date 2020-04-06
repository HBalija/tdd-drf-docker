from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'password123'
        user = self.UserModel.objects.create_user(email=email, password=password)

        self.assertTrue(self.UserModel.objects.exists())
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test new user email is normalized"""

        data = {
            'email': 'test@exAMPLe.com',
            'password': 'password123'
        }
        user = self.UserModel.objects.create_user(**data)

        self.assertTrue(self.UserModel.objects.exists())
        self.assertEqual(user.email, data['email'].lower())
