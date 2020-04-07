from rest_framework import serializers

from django.contrib.auth import get_user_model


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return UserModel.objects.create_user(**validated_data)
