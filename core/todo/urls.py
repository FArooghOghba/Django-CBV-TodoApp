from django.urls import path
from .views import (TaskListView, TaskCreateView, TaskUpdateView,
                    TaskDetailView, TaskDeleteView)


app_name = 'task'


urlpatterns = [
    path('', TaskListView.as_view(), name='list'),
    path('task/create/', TaskCreateView.as_view(), name='create'),
    path('task/detail/<int:task_id>/', TaskDetailView.as_view(), name='detail'),
    path('task/<int:task_id>/update/', TaskUpdateView.as_view(), name='update'),
    path('task/<int:task_id>/delete/', TaskDeleteView.as_view(), name='delete'),
]
