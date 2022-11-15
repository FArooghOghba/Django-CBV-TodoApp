from django.urls import path
from .views import TaskListView


app_name = 'Task'


urlpatterns = [
    path('', TaskListView.as_view(), name='list')
]
