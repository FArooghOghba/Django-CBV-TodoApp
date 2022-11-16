from django.urls import path
from .views import CustomLoginView, AccountsLogoutView


app_name = 'accounts'


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', AccountsLogoutView.as_view(), name='logout'),
]
