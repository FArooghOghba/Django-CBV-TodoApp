import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from todo.models import Task
from ..serializers import TaskModelSerializer


User = get_user_model()


@pytest.fixture
def test_user():
    user = User.objects.create_user(
        email='test@test.com',
        username='test_username',
        password='far!@#$%'
    )
    return user

@pytest.fixture
def test_task(test_user):
    task = Task.objects.create(
        user = test_user,
        title='test_title',
        descriptions='test_descriptions'
    )
    return task


@pytest.mark.django_db
class TestTodoAPISerializer:
    """
    Test with pytest for TaskModelSerializer.
    """
    client = APIClient()

    def test_task_list_serializer(self, test_user):
        url = reverse('task:api-v1:task-list')
        self.client.force_login(user=test_user)
        response = self.client.get(path=url)

        tasks = Task.objects.all()
        expected_data = TaskModelSerializer(
            tasks, many=True
        ).data

        assert response.data == expected_data

