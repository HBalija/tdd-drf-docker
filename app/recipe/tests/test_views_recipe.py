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
        self.payload = {
            'title': 'Cheese cake',
            'time_minutes': 30,
            'price': 5.00
        }

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

    def test_create_recipe(self):

        r = self.client.post(RECIPE_LIST_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=r.data['id'])

        for key in self.payload:
            self.assertEqual(self.payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        tag1 = create_tag(self.user, name='Dessert')
        tag2 = create_tag(self.user, name='Vegan')
        tag_payload = [tag1.id, tag2.id]
        self.payload['tags'] = tag_payload

        r = self.client.post(RECIPE_LIST_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=r.data['id'])

        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertTrue(all(tag.id in tag_payload for tag in tags))

    def test_create_recipe_with_ingredients(self):
        ing1 = create_ingredient(self.user, name='Chocolate')
        ing2 = create_ingredient(self.user, name='beer')
        ing_payload = [ing1.id, ing2.id]
        self.payload['ingredients'] = ing_payload

        r = self.client.post(RECIPE_LIST_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=r.data['id'])

        ings = recipe.ingredients.all()
        self.assertEqual(ings.count(), 2)
        self.assertTrue(all(ing.id in ing_payload for ing in ings))

    def test_partial_update_recipe(self):
        """ Test updating a recipe with patch """

        recipe = create_recipe(user=self.user)
        recipe.tags.add(create_tag(user=self.user))

        new_tag = create_tag(user=self.user, name='New tag')
        payload = dict(title='New title', tags=[new_tag.id])

        self.client.patch(get_recipe_detail_url(recipe.id), payload)
        recipe.refresh_from_db()

        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.tags.count(), 1)
        self.assertEqual(recipe.tags.first(), new_tag)

    def test_full_update_recipe(self):
        """ Test updating a recipe with put """

        recipe = create_recipe(user=self.user)
        recipe.tags.add(create_tag(user=self.user))

        new_tag = create_tag(user=self.user, name='New tag')
        payload = RecipeDetailSerializer(recipe).data
        payload['title'] = 'New title'
        payload['tags'] = [new_tag.id]

        self.client.put(get_recipe_detail_url(recipe.id), payload)
        recipe.refresh_from_db()

        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.tags.count(), 1)
        self.assertEqual(recipe.tags.first(), new_tag)
