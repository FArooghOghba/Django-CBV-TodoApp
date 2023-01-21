from rest_framework import serializers
from django.contrib.auth import get_user_model

from todo.models import Task


# Get user model
user = get_user_model()


class TaskModelSerializer(serializers.ModelSerializer):
    """
    Task Serializer creates from ModelSerializer.
    """
    snippet = serializers.ReadOnlyField(source='get_snippet')
    absolute_url = serializers.SerializerMethodField(
        method_name='get_absolute_url'
    )

    def get_absolute_url(self, task_obj):
        request = self.context.get('request')
        return request.build_absolute_uri(task_obj.pk)

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super(TaskModelSerializer, self).to_representation(instance)

        is_retrieve = request.parser_context.get('kwargs').get('pk')
        if is_retrieve is not None:
            rep.pop('snippet', None)
            rep.pop('absolute_url', None)
        else:
            rep.pop('descriptions', None)

        return rep

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['user'] = user.objects.get(id=user_id)
        return super(TaskModelSerializer, self).create(validated_data)

    class Meta:
        model = Task
        fields = (
            'id', 'user', 'title', 'snippet', 'absolute_url',
            'descriptions', 'complete', 'created_date'
        )
        read_only_fields = ('user',)
