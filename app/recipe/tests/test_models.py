from utils.help_test_utils import create_user
from unittest.mock import patch

from django.test import TestCase

from recipe.models import Ingredient, get_recipe_instance_file_path, Recipe, Tag


class TagTest(TestCase):

    def test_tag_str(self):
        tag = Tag.objects.create(user=create_user(), name='Vegan')
        self.assertEqual(str(tag), tag.name)


class IngredientTest(TestCase):

    def test_ingredient_str(self):
        ing = Ingredient.objects.create(user=create_user(), name='Potato')
        self.assertEqual(str(ing), ing.name)


class RecipeTest(TestCase):

    def test_recipe_str(self):
        recipe = Recipe.objects.create(
            user=create_user(), title='Baked steak', time_minutes=5, price=5.00)
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """ Test that image is saved in correct location """

        uuid = 'test-uuid'
        # mock return value
        mock_uuid.return_value = uuid

        file_path = get_recipe_instance_file_path(None, 'myimage.jpg')
        expected_path = f'uploads/recipe/{uuid}.jpg'

        self.assertEqual(file_path, expected_path)
