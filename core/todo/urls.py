from django.urls import path
from .views import TaskListView, TaskCreateView, TaskUpdateView


app_name = 'task'


urlpatterns = [
    path('list/', TaskListView.as_view(), name='list'),
    path('create/', TaskCreateView.as_view(), name='create'),
    path('<int:task_id>/update/', TaskUpdateView.as_view(), name='update'),
]
