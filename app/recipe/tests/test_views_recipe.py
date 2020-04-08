from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import reverse

from recipe.models import Recipe
from recipe.serializers import RecipeDetailSerializer, RecipeSerializer
from utils.help_test_utils import (
    create_ingredient, create_recipe, create_tag, create_user, get_recipe_detail_url
)


RECIPE_LIST_URL = reverse('recipe:recipe-list')


class PublicRecipesApiTests(TestCase):
    """ Test unauthenticated recipe API access """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test that authentication is required """
        r = self.client.get(RECIPE_LIST_URL)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipesApiTests(TestCase):
    """ Test authenticated recipe API access """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_list_recipes(self):
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        r = self.client.get(RECIPE_LIST_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, serializer.data)

    def test_recipes_limited_to_user(self):
        user = create_user(email='new_user@example.com', password='password123')
        create_recipe(user=user)
        create_recipe(user=self.user)

        self.assertEqual(Recipe.objects.count(), 2)

        r = self.client.get(RECIPE_LIST_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

    def test_recipe_detail(self):
        recipe = create_recipe(user=self.user)
        recipe.tags.add(create_tag(user=self.user))
        recipe.ingredients.add(create_ingredient(user=self.user))
        serializer = RecipeDetailSerializer(recipe)

        r = self.client.get(get_recipe_detail_url(recipe.id))
        self.assertEqual(r.data, serializer.data)
