from django.urls import path
from .views import TaskListView, TaskCreateView


app_name = 'task'


urlpatterns = [
    path('list/', TaskListView.as_view(), name='list'),
    path('create/', TaskCreateView.as_view(), name='create'),
]
