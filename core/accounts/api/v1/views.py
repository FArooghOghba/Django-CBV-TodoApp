from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, login

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as BaseObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED,
    HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
)

from jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from mail_templated import EmailMessage
from decouple import config

from ...utils import EmailThread
from .serializers import (
    LoginSerializer, RegistrationModelSerializer,
    CustomAuthTokenSerializer, CustomTokenObtainSerializer,
    ChangePasswordSerializer, AccountActivationResendSerializer
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

            activation_email = EmailMessage(
                'email/activation_account.tpl',
                {
                    'user': username,
                    'token': f'http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{token}/',
                },
                'sender@example.com',
                [email]
            )

            EmailThread(activation_email).start()

            data = {
                'email': email,
                'username': username,
            }
            return Response(data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_401_UNAUTHORIZED)


class AccountActivationConfirmAPIView(APIView):
    """
   Confirm Activation view to activate user account.
   This view should be accessible for authenticated users.
   """
    def get(self, request, token, *args, **kwargs):
        try:
            decoded_token = decode(jwt=token, key=config('SECRET_KEY'), algorithms=['HS256'])
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

        activation_email = EmailMessage(
            'email/activation_account.tpl',
            {
                'user': username,
                'token': f'http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{token}/',
            },
            'sender@example.com',
            [email]
        )
        EmailThread(activation_email).start()
        return Response(
            {'detail': 'Your activation resend successfully.'},
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



class LoginGenericAPIView(GenericAPIView):
    """
    Login view to get user credentials with "Session Authentication".
    This view should be accessible also for unauthenticated users.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user is not None and user.is_active:
                login(request, user)
                return Response(serializer.data, status=HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=HTTP_401_UNAUTHORIZED)


class ObtainAuthTokenAPIView(BaseObtainAuthToken):
    """
    get or create token view to get user credentials with "token authentication".
    This view should be accessible also for unauthenticated users.
    """
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'username': user.username
            }
        )


class DiscardAuthTokenAPIView(APIView):
    """
    delete token view for "token authentication".
    This view should be accessible for authenticated users.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    create and get token pair view to get user credentials with "JWT".
    This view should be accessible also for unauthenticated users.
    """
    serializer_class = CustomTokenObtainSerializer