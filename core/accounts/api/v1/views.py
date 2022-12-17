from django.contrib.auth import get_user_model, login, authenticate

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as BaseObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_202_ACCEPTED,
    HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT
)

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    LoginSerializer, RegistrationModelSerializer,
    CustomAuthTokenSerializer, CustomTokenObtainSerializer
)


class RegistrationGenericAPIView(GenericAPIView):
    """
    Register view to get user credentials.
    This view should be accessible also for unauthenticated users.
    """
    serializer_class = RegistrationModelSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            data = {
                'email': email,
                'username': username,
            }
            return Response(data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_401_UNAUTHORIZED)


class LoginGenericAPIView(GenericAPIView):
    """
    Login view to get user credentials with "session authentication".
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