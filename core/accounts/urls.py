from django.urls import path, include
from .views import (
    AccountsLoginView, AccountsLogoutView, AccountsRegisterFormView,
    AccountsPasswordChangeView, AccountsPasswordChangeDoneView
)


app_name = 'accounts'


urlpatterns = [
    path('register/', AccountsRegisterFormView.as_view(), name='register'),
    path('change-password/', AccountsPasswordChangeView.as_view(), name='password_change'),
    path('change-password-done/', AccountsPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('login/', AccountsLoginView.as_view(), name='login'),
    path('logout/', AccountsLogoutView.as_view(), name='logout'),

    path('api/v1/', include('accounts.api.v1.urls')),
]
