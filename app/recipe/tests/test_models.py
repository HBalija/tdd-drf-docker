from django.test import TestCase

from recipe.models import Ingredient, Tag
from utils.utils_test_helpers import create_sample_user


class TagTest(TestCase):

    def test_tag_str(self):
        """Test Tag string representation"""
        tag = Tag.objects.create(user=create_sample_user(), name='Vegan')

        self.assertEqual(str(tag), tag.name)


class IngredientTest(TestCase):

    def test_ingredient_str(self):
        """Test Ingredient string representation"""
        ing = Ingredient.objects.create(user=create_sample_user(), name='Potato')

        self.assertEqual(str(ing), ing.name)
