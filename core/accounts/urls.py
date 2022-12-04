from django.urls import path, include
from .views import AccountsLoginView, AccountsLogoutView, AccountsRegisterFormView


app_name = 'accounts'


urlpatterns = [
    path('register/', AccountsRegisterFormView.as_view(), name='register'),
    path('login/', AccountsLoginView.as_view(), name='login'),
    path('logout/', AccountsLogoutView.as_view(), name='logout'),

    path('api/v1/', include('accounts.api.v1.urls')),
]
