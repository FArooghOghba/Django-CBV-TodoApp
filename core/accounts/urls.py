from django.urls import path, include
from .views import (
    AccountsLoginView, AccountsLogoutView, AccountsRegisterFormView,
    AccountsPasswordChangeView, AccountsPasswordChangeDoneView,
    AccountsActivationEmailSendTemplateView, AccountActivationEmailResendFormView,
    AccountActivationConfirmTemplateView
)


app_name = 'accounts'


urlpatterns = [
    path('register/', AccountsRegisterFormView.as_view(), name='register'),

    path('activation/confirm/<str:token>/', AccountActivationConfirmTemplateView.as_view(), name='activation_confirm'),
    path('activation/send/', AccountsActivationEmailSendTemplateView.as_view(), name='activation_send'),
    path('activation/resend/', AccountActivationEmailResendFormView.as_view(), name='activation_resend'),

    path('change-password/', AccountsPasswordChangeView.as_view(), name='password_change'),
    path('change-password-done/', AccountsPasswordChangeDoneView.as_view(), name='password_change_done'),

    path('login/', AccountsLoginView.as_view(), name='login'),
    path('logout/', AccountsLogoutView.as_view(), name='logout'),

    path('api/v1/', include('accounts.api.v1.urls')),
]
