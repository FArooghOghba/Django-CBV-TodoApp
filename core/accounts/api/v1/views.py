from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED

from django.contrib.auth import get_user_model, login, authenticate

from .serializers import LoginSerializer, RegistrationModelSerializer


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
    Login view to get user credentials.
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
