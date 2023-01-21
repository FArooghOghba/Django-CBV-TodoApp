from django.contrib.auth import get_user_model

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK, HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
)

from jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from rest_framework_simplejwt.tokens import RefreshToken

from mail_templated import EmailMessage
from decouple import config

from ....utils import EmailThread
from ..serializers import (
    ChangePasswordSerializer, ResetPasswordSerializer,
    ResetPasswordConfirmSerializer
)


User = get_user_model()


class ResetPasswordConfirmGenericAPIView(GenericAPIView):
    """
    Confirm Reset Password view to change user's password.
    """
    serializer_class = ResetPasswordConfirmSerializer

    def put(self, request, token, *args, **kwargs):
        try:
            decoded_token = decode(
                jwt=token, key=config('SECRET_KEY'), algorithms=['HS256']
            )
            user_id = decoded_token.get('user_id')
        except ExpiredSignatureError:
            return Response(
                {'detail': 'Your token has been expired.'},
                status=HTTP_400_BAD_REQUEST
            )
        except InvalidSignatureError:
            return Response(
                {'detail': 'Your token is not valid.'},
                status=HTTP_400_BAD_REQUEST
            )

        user_obj = User.objects.get(pk=user_id)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']

            user_obj.set_password(new_password)
            user_obj.save()
            return Response(
                {'new_password': 'Password changed successfully.'},
                status=HTTP_202_ACCEPTED
            )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ResetPasswordGenericAPIView(GenericAPIView):
    """
    Reset Password view to request for changing user's password.
    """
    serializer_class = ResetPasswordSerializer

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        username = user.username
        email = user.email

        token = self.get_token_for_user(user)
        domain = 'http://127.0.0.1:8000/'
        url = 'accounts/api/v1/reset_password/confirm/'

        activation_email = EmailMessage(
            'email/reset_password.tpl',
            {
                'user': username,
                'token': f'{domain}{url}{token}/',
            },
            'sender@example.com',
            [email]
        )
        EmailThread(activation_email).start()
        return Response(
            {
                'detail': "We've emailed you a link for "
                          "resetting you password, "
                          "if you don't receive an email, "
                          "please make sure you've"
                          "entered the email address your "
                          "registered with."
            },
            status=HTTP_200_OK
        )


class ChangePasswordGenericAPIView(GenericAPIView):
    """
    Change Password view to get new password for user.
    This view should be accessible for authenticated users.
    """
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        user_obj = self.request.user
        return user_obj

    def put(self, request, *args, **kwargs):
        user_obj = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user_obj.check_password(old_password):
                return Response(
                    {'wrong password': 'Old password is not correct'},
                    status=HTTP_400_BAD_REQUEST
                )

            user_obj.set_password(new_password)
            user_obj.save()
            return Response(
                {'new_password': 'Password changed successfully.'},
                status=HTTP_202_ACCEPTED
            )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
