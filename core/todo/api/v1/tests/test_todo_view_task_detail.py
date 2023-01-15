import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED,
    HTTP_202_ACCEPTED, HTTP_200_OK
)
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

@pytest.fixture
def api_client():
   return APIClient()


@pytest.mark.django_db
class TestTodoAPITaskDetail:
    """
    Test with pytest for TaskModelViewset for
    task detail.
    """

    def test_get_task_detail_response_403_forbidden_status(self, api_client):
        """
        Test response of get request to task detail
        with unauthorized user.
        :return:
        """
        url = reverse(
            'task:api-v1:task-detail',
            kwargs={'pk': 1}
        )
        response = api_client.get(path=url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_get_task_detail_response_200_ok_status(
            self, api_client, test_user, test_task
    ):
        """
        Test response of get request to task detail
        with authorized user.
        :return:
        """
        url = reverse(
            'task:api-v1:task-detail',
            kwargs={'pk': test_task.pk}
        )
        api_client.force_login(user=test_user)
        response = api_client.get(path=url)
        assert response.status_code == HTTP_200_OK

    def test_delete_task_detail_response_200_ok_status(
            self, api_client, test_user, test_task
    ):
        """
        Test response of delete request to task detail
        with authorized user.
        :return:
        """
        url = reverse(
            'task:api-v1:task-detail',
            kwargs={'pk': test_task.pk}
        )
        api_client.force_login(user=test_user)
        response = api_client.get(path=url)
        assert response.status_code == HTTP_200_OK

    def test_put_task_detail_response_200_ok_status(
            self, api_client, test_user, test_task
    ):
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
        api_client.force_login(user=test_user)
        response = api_client.get(path=url)
        assert response.status_code == HTTP_200_OK

    def test_put_task_detail_response_403_unauthorized_status(
            self, api_client, test_task
    ):
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
        response = api_client.get(path=url)
        assert response.status_code == HTTP_403_FORBIDDEN