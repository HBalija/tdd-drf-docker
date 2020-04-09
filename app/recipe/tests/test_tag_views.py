from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import reverse

from recipe.models import Tag
from recipe.serializers import TagSerializer
from utils.help_test_utils import create_user, create_recipe, create_tag


TAG_LIST_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """ Test publicly available tags API """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login is required for retrieving tags """
        r = self.client.get(TAG_LIST_URL)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """ Test the authorized user tags API """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.payload = {'name': 'Test tag'}

    def test_list_tags(self):
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Desert')

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        r = self.client.get(TAG_LIST_URL)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, serializer.data)

    def test_tags_limited_to_user(self):
        tag = Tag.objects.create(user=self.user, name='Vegan')

        anonymous_user = create_user(email='anonymous@example.com', password='password123')
        Tag.objects.create(user=anonymous_user, name='Horse meat')

        self.assertEqual(Tag.objects.count(), 2)

        r = self.client.get(TAG_LIST_URL)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        r = self.client.post(TAG_LIST_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Tag.objects.filter(user=self.user, name=self.payload['name']).exists())

    def test_create_tag_invalid(self):
        """ Test creating a new tag with invalid payload """

        self.payload['name'] = ''
        r = self.client.post(TAG_LIST_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags_signed_to_recepies(self):
        tag1 = create_tag(user=self.user, name='breakfast')
        tag2 = create_tag(user=self.user, name='lunch')
        recipe = create_recipe(user=self.user, title='eggs with ham')

        recipe.tags.add(tag1)

        r = self.client.get(TAG_LIST_URL, {'assigned_only': 1})

        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)

        self.assertIn(serializer1.data, r.data)
        self.assertNotIn(serializer2.data, r.data)

    def test_retrive_tags_assigned_unique(self):
        tag1 = create_tag(user=self.user, name='breakfast')
        create_tag(user=self.user, name='lunch')

        recipe1 = create_recipe(user=self.user, title='pancakes')
        recipe2 = create_recipe(user=self.user, title='jam on toast')

        recipe1.tags.add(tag1)
        recipe2.tags.add(tag1)

        r = self.client.get(TAG_LIST_URL, {'assigned_only': 1})
        self.assertEqual(len(r.data), 1)
