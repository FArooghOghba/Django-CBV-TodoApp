from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


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
                    'Access denied: wrong username or password.',
                    code=HTTP_401_UNAUTHORIZED
                )

            if not user.is_verified:
                raise serializers.ValidationError(
                    'Verification: You are not verified your account yet.',
                    code=HTTP_401_UNAUTHORIZED
                )
        else:
            raise serializers.ValidationError(
                'Both "email" and "password" are required.',
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
    email = serializers.EmailField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label="Token",
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
                    'Unable to log in with provided credentials.',
                    code=HTTP_401_UNAUTHORIZED
                )

            if not user.is_verified:
                raise serializers.ValidationError(
                    'Verification: You are not verified your account yet.',
                    code=HTTP_401_UNAUTHORIZED
                )
        else:
            raise serializers.ValidationError(
                'Must include "username" and "password".',
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
                'Verification: You are not verified your account yet.',
                code=HTTP_401_UNAUTHORIZED
            )

        validated_data['user_id'] = self.user.id
        validated_data['email'] = self.user.email
        validated_data['username'] = self.user.username

        return validated_data
