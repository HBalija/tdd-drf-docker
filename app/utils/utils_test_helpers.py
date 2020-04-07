from django.contrib.auth import get_user_model


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_sample_user():
    data = dict(email="test@example.com", password="password123", name="Test name")
    return get_user_model().objects.create_user(**data)


def create_sample_superuser():
    return get_user_model().objects.create_superuser(
        email='admin@example.com', password='password123')
