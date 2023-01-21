import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient


User = get_user_model()


@pytest.fixture
def test_user():
    user = User.objects.create_user(
        email='test@test.com',
        username='test_username',
        password='far!@#$%'
    )
    return user


@pytest.mark.django_db
class TestTodoAPITaskList:
    """
    Test with pytest for TaskModelViewset for task list.
    """
    client = APIClient()
    data = {
        'title': 'test_title',
        'descriptions': 'test_descriptions'
    }

    def test_get_task_list_unauthorized_response_403_forbidden_status(self):
        """
        Test response of get request task list for unauthorized user.
        :return:
        """
        url = reverse('task:api-v1:task-list')
        response = self.client.get(path=url)
        assert response.status_code == 403

    def test_get_task_list_authorized_response_200_ok_status(self, test_user):
        """
        Test response of get request task list for authorized user.
        :return:
        """
        url = reverse('task:api-v1:task-list')
        self.client.force_login(user=test_user)
        response = self.client.get(path=url)
        assert response.status_code == 200

    def test_post_create_task_response_400_bad_request_status(self, test_user):
        """
        Test response of post request to task list to create task
        with bad data.
        :return:
        """
        url = reverse('task:api-v1:task-list')
        self.client.force_login(user=test_user)
        data = {}
        response = self.client.post(
            path=url,
            data=data
        )
        assert response.status_code == 400

    def test_post_create_task_response_201_created_status(self, test_user):
        """
        Test response of post request to task list to create task
        with correct data and authorized user.
        :return:
        """
        url = reverse('task:api-v1:task-list')
        self.client.force_login(user=test_user)
        data = self.data
        response = self.client.post(
            path=url,
            data=data
        )
        assert response.status_code == 201
