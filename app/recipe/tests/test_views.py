from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import reverse

from recipe.models import Tag
from recipe.serializers import TagSerializer
from utils.utils_test_helpers import create_sample_user, create_user


TAG_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        r = self.client.get(TAG_URL)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = create_sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.payload = {'name': 'Test tag'}

    def test_list_tags(self):
        """Test listing tags"""

        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Desert')

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        r = self.client.get(TAG_URL)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""

        Tag.objects.create(user=self.user, name='Vegan')

        anonymous_user = create_user(email='anonymous@example.com', password='password123')

        Tag.objects.create(user=anonymous_user, name='Horse meat')

        self.assertEqual(Tag.objects.count(), 2)

        r = self.client.get(TAG_URL)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        r = self.client.post(TAG_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Tag.objects.filter(user=self.user, name=self.payload['name']).exists())

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        self.payload['name'] = ''
        r = self.client.post(TAG_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
