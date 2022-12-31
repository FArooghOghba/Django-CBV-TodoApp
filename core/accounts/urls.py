from django.urls import path, include
from .views import (
    AccountsLoginView, AccountsLogoutView, AccountsRegisterFormView,
    AccountsPasswordChangeView, AccountsPasswordChangeDoneView,
    AccountsActivationEmailSendTemplateView, AccountActivationEmailResendFormView,
    AccountActivationConfirmTemplateView, AccountPasswordResetView,
    AccountPasswordResetDoneView, AccountPasswordResetConfirmView,
    AccountPasswordResetCompleteView
)


app_name = 'accounts'


urlpatterns = [
    # Registration
    path('register/', AccountsRegisterFormView.as_view(), name='register'),

    # Activation Account
    path('activation/confirm/<str:token>/', AccountActivationConfirmTemplateView.as_view(), name='activation_confirm'),
    path('activation/send/', AccountsActivationEmailSendTemplateView.as_view(), name='activation_send'),
    path('activation/resend/', AccountActivationEmailResendFormView.as_view(), name='activation_resend'),

    # Reset Password
    path('password_reset/', AccountPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', AccountPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', AccountPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', AccountPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Change Password
    path('password_change/', AccountsPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', AccountsPasswordChangeDoneView.as_view(), name='password_change_done'),

    path('login/', AccountsLoginView.as_view(), name='login'),
    path('logout/', AccountsLogoutView.as_view(), name='logout'),

    path('api/v1/', include('accounts.api.v1.urls')),
]
