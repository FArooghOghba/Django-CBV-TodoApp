from django.contrib.auth import get_user_model, login

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED
)

from rest_framework_simplejwt.views import TokenObtainPairView

from ..serializers import (
    LoginSerializer, CustomAuthTokenSerializer,
    CustomTokenObtainSerializer,
)


User = get_user_model()


# Login Session Authentication
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


# Token Authentication
class CustomObtainAuthTokenView(ObtainAuthToken):
    """
    get or create token view to get user credentials with "Token Authentication".
    This view should be accessible also for unauthenticated users.
    """
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username': user.username
            }
        )


# Discard Token Authentication
class DiscardAuthTokenAPIView(APIView):
    """
    delete token view for "Token Authentication".
    This view should be accessible for authenticated users.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_204_NO_CONTENT)


# JWT Authentication
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    create and get token pair view to get user credentials with "JWT".
    This view should be accessible also for unauthenticated users.
    """
    serializer_class = CustomTokenObtainSerializer