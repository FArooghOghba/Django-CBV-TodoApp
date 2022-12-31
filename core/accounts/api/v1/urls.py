from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (
    LoginGenericAPIView, RegistrationGenericAPIView,
    CustomObtainAuthTokenView, DiscardAuthTokenAPIView,
    CustomTokenObtainPairView, ChangePasswordGenericAPIView,
    AccountActivationConfirmAPIView, AccountActivationResendGenericAPIView,
    ResetPasswordGenericAPIView, ResetPasswordConfirmGenericAPIView
)


app_name = 'api-v1'


urlpatterns = [
    # Registration
    path('register/', RegistrationGenericAPIView.as_view(), name='register'),

    # Activation Email
    path('activation/confirm/<str:token>/', AccountActivationConfirmAPIView.as_view(), name='activation-confirm'),
    path('activation/resend/', AccountActivationResendGenericAPIView.as_view(), name='activation-resend'),

    # Reset Password Manager With JWT
    path('reset_password/', ResetPasswordGenericAPIView.as_view(), name='reset_password'),
    path('reset_password/confirm/<str:token>/', ResetPasswordConfirmGenericAPIView.as_view(), name='reset_password_confirm'),

    # Change Password
    path('change_password/', ChangePasswordGenericAPIView.as_view(), name='change-password'),

    # Session Authentication
    path('session/login/', LoginGenericAPIView.as_view(), name='session-login'),

    # Token Authentication
    path('token/login/', CustomObtainAuthTokenView.as_view(), name='token-login'),
    path('token/logout/', DiscardAuthTokenAPIView.as_view(), name='token-logout'),

    # JWT Authentication
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
]
