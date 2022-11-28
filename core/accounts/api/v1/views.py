from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED

from django.contrib.auth import login

from .serializers import LoginSerializer


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
