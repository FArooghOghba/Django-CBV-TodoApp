from rest_framework import serializers
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


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


class RegistrationModelSerializer(serializers.ModelSerializer):
    """
    This serializer defines four fields for registration:
      * email
      * username
      * password.
    It will try to register the user with, when validated.
    """
    password = serializers.CharField(
        max_length=255,
        validators=[validate_password],
        style={'input_type': 'password'},
        write_only=True
    )
    password_confirm = serializers.CharField(
        max_length=255,
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model= User
        fields = ('email', 'username', 'password', 'password_confirm')

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if not password == password_confirm:
            raise serializers.ValidationError(
                _('Passwords must be the same.'),
                code=HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(
            Q(email=email) | Q(username=username)
        ).exists()

        if user:
            raise serializers.ValidationError(
                _('User exists, login or choose another email.'),
                code=HTTP_400_BAD_REQUEST
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        return User.objects.create_user(**validated_data)
