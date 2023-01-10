from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED,
    HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)

from jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from rest_framework_simplejwt.tokens import RefreshToken

from mail_templated import EmailMessage
from decouple import config

from ....utils import EmailThread
from ..serializers import (
    RegistrationModelSerializer, AccountActivationResendSerializer,
)


User = get_user_model()


class RegistrationGenericAPIView(GenericAPIView):
    """
    Register view to get user credentials.
    This view should be accessible also for unauthenticated users.
    """
    serializer_class = RegistrationModelSerializer

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            user_obj = get_object_or_404(User, email=email)

            token = self.get_token_for_user(user_obj)
            domain = 'http://127.0.0.1:8000/'
            url = 'accounts/api/v1/activation/confirm/'

            activation_email = EmailMessage(
                template_name='email/activation_account.tpl',
                context={
                    'user': username,
                    'token': f'{domain}{url}{token}/',
                },
                from_email='sender@example.com',
                to=[email]
            )

            EmailThread(activation_email).start()

            data = {
                'detail': 'Your activation email sent to your inbox.',
                'email': email,
                'username': username,
            }
            return Response(
                data, status=HTTP_201_CREATED
            )

        return Response(serializer.errors, status=HTTP_401_UNAUTHORIZED)

class AccountActivationConfirmAPIView(APIView):
    """
    Confirm Activation view to activate user account.
    This view should be accessible for authenticated users.
    """
    def get(self, request, token, *args, **kwargs):
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

        user = User.objects.get(pk=user_id)
        if user.is_verified:
            return Response(
                {'detail': 'Your account has already verified.'},
                status=HTTP_400_BAD_REQUEST
            )

        user.is_verified = True
        user.save()

        return Response(
            {'detail': 'Your account have been verified successfully.'},
            status=HTTP_202_ACCEPTED
        )

class AccountActivationResendGenericAPIView(GenericAPIView):
    serializer_class = AccountActivationResendSerializer

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
        url = 'accounts/api/v1/activation/confirm/'

        activation_email = EmailMessage(
            'email/activation_account.tpl',
            {
                'user': username,
                'token': f'{domain}{url}{token}/',
            },
            'sender@example.com',
            [email]
        )
        EmailThread(activation_email).start()
        return Response(
            {'detail': 'Your activation resend successfully.'},
            status=HTTP_200_OK
        )
