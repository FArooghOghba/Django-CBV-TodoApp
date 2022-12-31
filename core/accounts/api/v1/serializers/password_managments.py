from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST


User = get_user_model()


# Reset Password
class ResetPasswordSerializer(serializers.Serializer):
    """
    This serializer defines one fields for "Reset Password":
      * email
    It will try to get user email with, when validated.
    """
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'detail': 'An invalid email has been entered.'}
            )

        attrs['user'] = user_obj
        return super().validate(attrs)


# Reset Password Confirm
class ResetPasswordConfirmSerializer(serializers.Serializer):
    """
    This serializer defines two fields for "Confirm Reset Password":
      * new_password
      * confirm_new_password.
    It will try to change user password with, when validated.
    """
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
