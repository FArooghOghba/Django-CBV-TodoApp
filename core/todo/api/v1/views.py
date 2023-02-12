import requests

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from todo.models import Task
from .serializers import TaskModelSerializer
from .permissions import IsTaskOwner

from decouple import config


class TaskModelViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing the tasks
    associated with the user.
    """
    serializer_class = TaskModelSerializer
    permission_classes = [IsAuthenticated, IsTaskOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['complete']
    search_fields = ['title', 'descriptions']
    ordering_fields = ['complete', 'created_date']

    def get_queryset(self):
        user_id = self.request.user.id
        return Task.objects.filter(user__id=user_id)


class WeatherAPIView(APIView):
    @method_decorator(cache_page(60 * 20, key_prefix="weather-view"))
    def get(self, request):
        city_name = config('CITY_NAME')
        api_key = config('OPEN_WEATHER_API_KEY')
        units = config('UNITS')
        open_weather_url = f"https://api.openweathermap.org/data/2.5/weather?" \
                           f"q={city_name}&appid={api_key}&units={units}"

        response = requests.get(url=open_weather_url)

        return JsonResponse(response.json())

