from django.contrib.auth import get_user_model
from django.urls import reverse

from recipe.models import Ingredient, Recipe, Tag


def create_user(**params):
    defaults = dict(email="test@example.com", password="password123", name="Test name")
    defaults.update(params)
    return get_user_model().objects.create_user(**defaults)


def create_superuser():
    return get_user_model().objects.create_superuser(
        email='admin@example.com', password='password123')


def create_tag(user, name='Main course'):
    return Tag.objects.create(user=user, name=name)


def create_ingredient(user, name='Cinnamon'):
    return Ingredient.objects.create(user=user, name=name)


def create_recipe(user, **params):
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


def get_recipe_detail_url(recipe_id):
    """ Return recipe detail url """
    return reverse('recipe:recipe-detail', kwargs={'pk': recipe_id})


def get_image_upload_url(recipe_id):
    """ Return URL for recipe image upload """
    return reverse('recipe:recipe-upload-image', args=[recipe_id])
