from django.urls import path

from .views import (
    LoginGenericAPIView, RegistrationGenericAPIView,
    ObtainAuthTokenAPIView, DiscardAuthTokenAPIView
)


app_name = 'api-v1'


urlpatterns = [
    # Registration
    path('register/', RegistrationGenericAPIView.as_view(), name='register'),

    # Session Authentication
    path('session/login/', LoginGenericAPIView.as_view(), name='session-login'),

    # Token Authentication
    path('token/login/', ObtainAuthTokenAPIView.as_view(), name='token-login'),
    path('token/logout/', DiscardAuthTokenAPIView.as_view(), name='token-logout'),
]
