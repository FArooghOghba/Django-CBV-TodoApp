from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (
    LoginGenericAPIView, RegistrationGenericAPIView,
    ObtainAuthTokenAPIView, DiscardAuthTokenAPIView,
    CustomTokenObtainPairView, ChangePasswordGenericAPIView
)


app_name = 'api-v1'


urlpatterns = [
    # Registration
    path('register/', RegistrationGenericAPIView.as_view(), name='register'),

    # Change Password
    path('change_password/', ChangePasswordGenericAPIView.as_view(), name='change-password'),

    # Session Authentication
    path('session/login/', LoginGenericAPIView.as_view(), name='session-login'),

    # Token Authentication
    path('token/login/', ObtainAuthTokenAPIView.as_view(), name='token-login'),
    path('token/logout/', DiscardAuthTokenAPIView.as_view(), name='token-logout'),

    # JWT Authentication
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
]
