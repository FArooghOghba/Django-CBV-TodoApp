from rest_framework.serializers import ModelSerializer

from todo.models import Task


class TaskModelSerializer(ModelSerializer):
    """
    Task Serializer creates from ModelSerializer.
    """
    class Meta:
        model = Task
        fields = (
            'id', 'user', 'title', 'descriptions', 'complete', 'created_date'
        )
