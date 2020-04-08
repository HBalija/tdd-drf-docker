from django.test import TestCase

from recipe.models import Ingredient, Recipe, Tag
from utils.utils_test_helpers import create_sample_user


class TagTest(TestCase):

    def test_tag_str(self):
        tag = Tag.objects.create(user=create_sample_user(), name='Vegan')
        self.assertEqual(str(tag), tag.name)


class IngredientTest(TestCase):

    def test_ingredient_str(self):
        ing = Ingredient.objects.create(user=create_sample_user(), name='Potato')
        self.assertEqual(str(ing), ing.name)


class RecipeTest(TestCase):

    def test_recipe_str(self):
        recipe = Recipe.objects.create(
            user=create_sample_user(), title='Baked steak', time_minutes=5, price=5.00)
        self.assertEqual(str(recipe), recipe.title)
