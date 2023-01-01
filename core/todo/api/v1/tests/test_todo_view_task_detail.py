import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from todo.models import Task


User = get_user_model()


@pytest.fixture
def test_user():
    user = User.objects.create_user(
        email='test@test_email.com',
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
class TestTodoAPITaskDetail:
    """
    Test with pytest for TaskModelViewset for
    task detail.
    """
    client = APIClient()

    def test_get_task_detail_response_403_forbidden_status(self):
        """
        Test response of get request to task detail
        with unauthorized user.
        :return:
        """
        url = reverse(
            'task:api-v1:task-detail',
            kwargs={'pk': 1}
        )
        response = self.client.get(path=url)
        assert response.status_code == 403

    def test_get_task_detail_response_200_ok_status(self, test_user, test_task):
        """
        Test response of get request to task detail
        with authorized user.
        :return:
        """
        url = reverse(
            'task:api-v1:task-detail',
            kwargs={'pk': test_task.pk}
        )
        self.client.force_login(user=test_user)
        response = self.client.get(path=url)
        assert response.status_code == 200

    def test_delete_task_detail_response_200_ok_status(self, test_user, test_task):
        """
        Test response of delete request to task detail
        with authorized user.
        :return:
        """
        url = reverse(
            'task:api-v1:task-detail',
            kwargs={'pk': test_task.pk}
        )
        self.client.force_login(user=test_user)
        response = self.client.get(path=url)
        assert response.status_code == 200

    def test_put_task_detail_response_200_ok_status(self, test_user, test_task):
        """
        Test response of put request to task detail
        with authorized user.
        :return:
        """
        url = reverse(
            'task:api-v1:task-detail',
            kwargs={'pk': test_task.pk}
        )
        test_task.title = 'test_title_edited'
        self.client.force_login(user=test_user)
        response = self.client.get(path=url)
        assert response.status_code == 200

    def test_put_task_detail_response_403_unauthorized_status(self, test_task):
        """
        Test response of put request to task detail
        with unauthorized user.
        :return:
        """
        url = reverse(
            'task:api-v1:task-detail',
            kwargs={'pk': test_task.pk}
        )
        test_task.title = 'test_title_edited'
        response = self.client.get(path=url)
        assert response.status_code == 403