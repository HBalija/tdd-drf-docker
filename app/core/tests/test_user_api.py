from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


CREATE_USER_URL = reverse('core:create')
TOKEN_URL = reverse('core:token')


UserModel = get_user_model()


def create_user(**params):
    return UserModel.objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()
        self.payload = dict(email="test@example.com", password="password123", name="Test name")

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""

        r = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        user = UserModel.objects.get(**r.data)
        self.assertTrue(user.check_password(self.payload['password']))
        # check that response data dict doesn't contain password key
        self.assertNotIn('password', r.data)

    def test_user_exists(self):
        """test creating user that already exists (email) fails"""

        create_user(**self.payload)

        r = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 character"""
        self.payload['password'] = 'pw'
        r = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(UserModel.objects.filter(email=self.payload['email']).exists())

    def test_create_token_for_user(self):
        """Test that token is created for the user"""

        create_user(**self.payload)

        r = self.client.post(TOKEN_URL, self.payload)
        self.assertIn('token', r.data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credantials(self):
        """Test that token is not created if invalid credentials"""

        create_user(**self.payload)
        self.payload['password'] = 'wrong'

        r = self.client.post(TOKEN_URL, self.payload)
        self.assertNotIn('token', r.data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exist"""
        r = self.client.post(TOKEN_URL, self.payload)
        self.assertNotIn('token', r.data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        r = self.client.post(TOKEN_URL, {})
        self.assertNotIn('token', r.data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
