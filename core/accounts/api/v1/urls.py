from django.urls import path

from .views import LoginGenericAPIView, RegisterGenericAPIView


app_name = 'api-v1'


urlpatterns = [
    path('register/', RegisterGenericAPIView.as_view(), name='register'),
    path('login/', LoginGenericAPIView.as_view(), name='login'),
]
