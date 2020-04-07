from rest_framework import generics

from core.serializers import UserSerializer


class CreateuserView(generics.CreateAPIView):
    """Create an new user"""
    serializer_class = UserSerializer
