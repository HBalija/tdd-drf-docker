from rest_framework import serializers

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _


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


class AuthTokenSerializer(serializers.Serializer):
    """Seriaizer for user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False  # default True
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')  # drf handles response

        attrs['user'] = user
        return attrs
