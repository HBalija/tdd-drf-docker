from django.test import TestCase

from recipe.models import Tag
from utils.utils_test_helpers import create_sample_user


class TagTest(TestCase):

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = Tag.objects.create(user=create_sample_user(), name='Vegan')

        self.assertEqual(str(tag), tag.name)
