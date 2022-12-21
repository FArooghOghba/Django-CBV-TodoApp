from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


# Registrations
class RegistrationModelSerializer(serializers.ModelSerializer):
    """
    This serializer defines four fields for registration:
      * email
      * username
      * password
      * password_confirm
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


class AccountActivationResendSerializer(serializers.Serializer):
    """
    This serializer defines a field for resending account activation email:
      * email
    It will try to resend email activation to the user when validated.
    """
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'detail': 'user does not exist.'}
            )

        if user_obj.is_verified:
            raise serializers.ValidationError(
                {'detail': 'Your account has already verified.'},
                code=HTTP_400_BAD_REQUEST
            )

        attrs['user'] = user_obj
        return super().validate(attrs)


# Change Password
class ChangePasswordSerializer(serializers.Serializer):
    """
    This serializer defines three fields for "Change Password":
      * old_password
      * new_password
      * confirm_new_password.
    It will try to change user password with, when validated.
    """
    old_password = serializers.CharField(
        max_length=255, write_only=True, required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        max_length=255, write_only=True, required=True,
        validators=[validate_password], style={'input_type': 'password'}
    )
    confirm_new_password = serializers.CharField(
        max_length=255, write_only=True, required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if not new_password == confirm_new_password:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match"},
                code=HTTP_400_BAD_REQUEST
            )

        return super().validate(attrs)


# Login For Session Authentication
class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for "session authentication":
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

            if not user.is_verified:
                raise serializers.ValidationError(
                    _('Verification: You are not verified your account yet.'),
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


# Token Authentications
class CustomAuthTokenSerializer(serializers.Serializer):
    """
    This serializer defines three fields for "Token Authentication":
      * email
      * password
      * token.
    It will try to authenticate to give a token to the user.
    """
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )

            # The "authenticate" call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                raise serializers.ValidationError(
                    _('Unable to log in with provided credentials.'),
                    code=HTTP_401_UNAUTHORIZED
                )

            if not user.is_verified:
                raise serializers.ValidationError(
                    _('Verification: You are not verified your account yet.'),
                    code=HTTP_401_UNAUTHORIZED
                )
        else:
            raise serializers.ValidationError(
                _('Must include "username" and "password".'),
                code=HTTP_401_UNAUTHORIZED
            )

        attrs['user'] = user
        return attrs


# JWT Authentications
class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    """
     This serializer adds three fields to validated data apart from
      the pair of tokens "JWT authentication":
      * user_id
      * email
      * username.
    It will try to authenticate to give a pair of tokens to the user.
    """

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        if not self.user.is_verified:
            raise serializers.ValidationError(
                _('Verification: You are not verified your account yet.'),
                code=HTTP_401_UNAUTHORIZED
            )

        validated_data['user_id'] = self.user.id
        validated_data['email'] = self.user.email
        validated_data['username'] = self.user.username

        return validated_data
