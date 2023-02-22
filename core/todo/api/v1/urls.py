from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TaskModelViewSet, WeatherAPIView


app_name = 'api-v1'

router = DefaultRouter()
router.register('task', TaskModelViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('weather/', WeatherAPIView.as_view(), name='weather'),
]
