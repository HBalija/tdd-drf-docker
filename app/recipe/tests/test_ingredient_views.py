from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import reverse

from recipe.models import Ingredient
from recipe.serializers import IngredientSerializer
from utils.help_test_utils import create_user, create_ingredient, create_recipe


INGREDIENT_LIST_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login is required for retrieving ingredients """
        r = self.client.get(INGREDIENT_LIST_URL)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """ Test the authorized user ingredients API """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.payload = {'name': 'Test ingredient'}

    def test_list_ingredients(self):
        Ingredient.objects.create(user=self.user, name='beer')
        Ingredient.objects.create(user=self.user, name='tobacco')

        ings = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ings, many=True)

        r = self.client.get(INGREDIENT_LIST_URL)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, serializer.data)

    def test_list_ingredients_limited_to_user(self):
        ing = Ingredient.objects.create(user=self.user, name='salt')

        anonymous_user = create_user(email='anonymous@example.com', password='password123')
        Ingredient.objects.create(user=anonymous_user, name='Horse meat')

        self.assertEqual(Ingredient.objects.count(), 2)

        r = self.client.get(INGREDIENT_LIST_URL)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]['name'], ing.name)

    def test_create_ingredient_successful(self):
        r = self.client.post(INGREDIENT_LIST_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Ingredient.objects.filter(
            user=self.user, name=self.payload['name']).exists())

    def test_create_tag_invalid(self):
        """ Test creating a new ingredient with invalid payload """
        self.payload['name'] = ''
        r = self.client.post(INGREDIENT_LIST_URL, self.payload)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ingredients_signed_to_recepies(self):
        ing1 = create_ingredient(user=self.user, name='eggs')
        ing2 = create_ingredient(user=self.user, name='potato')
        recipe = create_recipe(user=self.user, title='eggs with ham')

        recipe.ingredients.add(ing1)

        r = self.client.get(INGREDIENT_LIST_URL, {'assigned_only': 1})

        serializer1 = IngredientSerializer(ing1)
        serializer2 = IngredientSerializer(ing2)

        self.assertIn(serializer1.data, r.data)
        self.assertNotIn(serializer2.data, r.data)

    def test_retrive_ingredients_assigned_unique(self):
        ing1 = create_ingredient(user=self.user, name='toast')
        create_ingredient(user=self.user, name='tomato')

        recipe1 = create_recipe(user=self.user, title='pancakes')
        recipe2 = create_recipe(user=self.user, title='jam on toast')

        recipe1.ingredients.add(ing1)
        recipe2.ingredients.add(ing1)

        r = self.client.get(INGREDIENT_LIST_URL, {'assigned_only': 1})
        self.assertEqual(len(r.data), 1)
