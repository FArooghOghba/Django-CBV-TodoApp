from django.urls import path, include
from .views import (TaskListView, TaskCreateView, TaskUpdateView,
                    TaskDetailView, TaskDeleteView, TaskCompleteView)


app_name = 'task'


urlpatterns = [
    path('', TaskListView.as_view(), name='list'),
    path('create/', TaskCreateView.as_view(), name='create'),
    path('detail/<int:task_id>/', TaskDetailView.as_view(), name='detail'),
    path('<int:task_id>/update/', TaskUpdateView.as_view(), name='update'),
    path('<int:task_id>/delete/', TaskDeleteView.as_view(), name='delete'),
    path(
        '<int:task_id>/complete/', TaskCompleteView.as_view(), name='complete'
    ),

    path('api/v1/', include('todo.api.v1.urls'))
]
