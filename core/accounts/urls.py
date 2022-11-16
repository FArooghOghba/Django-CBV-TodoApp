from django.urls import path
from .views import AccountsLoginView, AccountsLogoutView


app_name = 'accounts'


urlpatterns = [
    path('login/', AccountsLoginView.as_view(), name='login'),
    path('logout/', AccountsLogoutView.as_view(), name='logout'),
]
