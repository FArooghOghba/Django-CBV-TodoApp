from django.urls import path
from .views import (TaskListView, TaskCreateView, TaskUpdateView,
                    TaskDetailView, TaskDeleteView)


app_name = 'task'


urlpatterns = [
    path('list/', TaskListView.as_view(), name='list'),
    path('create/', TaskCreateView.as_view(), name='create'),
    path('detail/<int:task_id>/', TaskDetailView.as_view(), name='detail'),
    path('<int:task_id>/update/', TaskUpdateView.as_view(), name='update'),
    path('<int:task_id>/delete/', TaskDeleteView.as_view(), name='delete'),
]
