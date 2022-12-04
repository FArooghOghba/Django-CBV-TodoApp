from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from todo.models import Task
from .serializers import TaskModelSerializer
from .permissions import IsTaskOwner


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
