from django.urls import path

from .views import LoginGenericAPIView, RegistrationGenericAPIView


app_name = 'api-v1'


urlpatterns = [
    path('register/', RegistrationGenericAPIView.as_view(), name='register'),
    path('login/', LoginGenericAPIView.as_view(), name='login'),
]
