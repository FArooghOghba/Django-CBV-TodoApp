from rest_framework import serializers
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * email
      * password.
    It will try to authenticate the user with when validated.
    """
    email = serializers.EmailField(max_length=128)
    password = serializers.CharField(
        max_length=255,
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=request, email=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    _('Access denied: wrong username or password.'),
                    code=HTTP_401_UNAUTHORIZED
                )
        else:
            raise serializers.ValidationError(
                _('Both "email" and "password" are required.'),
                code=HTTP_400_BAD_REQUEST
            )

        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.Serializer):
    """
    This serializer defines three fields for registration:
      * email
      * password.
    It will try to register the user with, when validated.
    """
    email = serializers.EmailField(max_length=128)
    username = serializers.CharField(max_length=255)
    password1 = serializers.CharField(
        max_length=255,
        style={'input_type': 'password'},
        write_only=True
    )
    password2 = serializers.CharField(
        max_length=255,
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if not password1 == password2:
            raise serializers.ValidationError(
                _('Passwords must be the same.'),
                code=HTTP_401_UNAUTHORIZED
            )

        user = get_user_model().objects.filter(
            Q(email=email) | Q(username=username)
        ).exists()

        if user:
            raise serializers.ValidationError(
                _('User exists, login or choose another email.'),
                code=HTTP_401_UNAUTHORIZED
            )

        return attrs
