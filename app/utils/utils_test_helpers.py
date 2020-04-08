from django.contrib.auth import get_user_model

from recipe.models import Recipe


def create_sample_user(**params):
    defaults = dict(email="test@example.com", password="password123", name="Test name")
    defaults.update(params)
    return get_user_model().objects.create_user(**defaults)


def create_sample_superuser():
    return get_user_model().objects.create_superuser(
        email='admin@example.com', password='password123')


def create_sample_recipe(user, **params):
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)
