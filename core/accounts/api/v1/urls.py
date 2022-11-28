from django.urls import path

from .views import LoginGenericAPIView


app_name = 'api-v1'


urlpatterns = [
    path('login/', LoginGenericAPIView.as_view(), name='login')
]
