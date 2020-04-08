from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from utils.help_test_utils import create_user

CREATE_USER_URL = reverse('core:create')
TOKEN_URL = reverse('core:token')
USER_DETAIL_URL = reverse('core:detail')


UserModel = get_user_model()


class PublicUserApiTest(TestCase):
    """ Test users public API """

    def setUp(self):
        self.client = APIClient()
        self.payload = dict(email="test@example.com", password="password123", name="Test name")

    def test_create_valid_user_success(self):
        r = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        user = UserModel.objects.get(**r.data)
        self.assertTrue(user.check_password(self.payload['password']))
        # check that response data dict doesn't contain password key
        self.assertNotIn('password', r.data)

    def test_user_exists(self):
        """ test creating user that already exists fails """

        create_user(**self.payload)
        r = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test that password must be more than 5 characters """

        self.payload['password'] = 'pw'
        r = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(UserModel.objects.filter(email=self.payload['email']).exists())

    def test_create_token_for_user(self):
        create_user(**self.payload)
        r = self.client.post(TOKEN_URL, self.payload)
        self.assertIn('token', r.data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credantials(self):
        create_user(**self.payload)
        self.payload['password'] = 'wrong'
        r = self.client.post(TOKEN_URL, self.payload)
        self.assertNotIn('token', r.data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        r = self.client.post(TOKEN_URL, self.payload)
        self.assertNotIn('token', r.data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Test that email and password are required """
        r = self.client.post(TOKEN_URL, {})
        self.assertNotIn('token', r.data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        r = self.client.get(USER_DETAIL_URL)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.payload = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Name'
        }
        self.user = create_user(**self.payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        r = self.client.get(USER_DETAIL_URL)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, {'name': self.user.name, 'email': self.user.email})

    def test_post_user_detail_not_allowed(self):
        r = self.client.post(USER_DETAIL_URL, {})
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        self.payload['name'] = 'New name'
        self.payload['password'] = 'newpassword123'

        r = self.client.patch(USER_DETAIL_URL, self.payload)

        self.user.refresh_from_db()  # get user after patch request

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, self.payload['name'])
        self.assertTrue(self.user.check_password(self.payload['password']))
