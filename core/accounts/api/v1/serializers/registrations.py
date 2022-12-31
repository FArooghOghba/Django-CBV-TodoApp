from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q

from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST


User = get_user_model()


# Registrations
class RegistrationModelSerializer(serializers.ModelSerializer):
    """
    This serializer defines four fields for registration:
      * email
      * username
      * password
      * password_confirm
    It will try to register the user and send email with, when validated.
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
                'Passwords must be the same.',
                code=HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(
            Q(email=email) | Q(username=username)
        ).exists()

        if user:
            raise serializers.ValidationError(
                'User exists, login or choose another email.',
                code=HTTP_400_BAD_REQUEST
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        return User.objects.create_user(**validated_data)


# Account Activation resend
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
