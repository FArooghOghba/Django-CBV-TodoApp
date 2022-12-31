import pytest
from django.urls import reverse
from rest_framework.test import APIClient


class TestTodoAPIApp:
    client = APIClient()

    def test_get_task_list_view_response_200_ok_status(self):
        url = reverse('task:api-v1:task-list')
        response = self.client.get(path=url)
        assert response.status_code == 403
