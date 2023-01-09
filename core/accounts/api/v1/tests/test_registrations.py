import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_401_UNAUTHORIZED,
)


User = get_user_model()


@pytest.fixture
def api_client():
   return APIClient()


@pytest.mark.django_db
class TestAccountsAPIRegistrations:
    @pytest.mark.parametrize(
        'email, username, password, confirm_password, status_code', [
            ('test_email@test.com', 'test_user', '123', '123', HTTP_401_UNAUTHORIZED),
            ('test_email@test.com', 'test_user', 'far!@#$%', 'wrong_pass', HTTP_401_UNAUTHORIZED),
            ('wrong_email', '', 'far!@#$%', 'far!@#$%', HTTP_401_UNAUTHORIZED),
            ('test_email@test.com', 'test_user', 'far!@#$%', 'far!@#$%', HTTP_201_CREATED),
        ]
    )
    def test_accounts_api_register_view(
            self, api_client, email,
            username, password, confirm_password,
            status_code
    ):

        url = reverse('accounts:api-v1:register')
        data = {
            'email': email,
            'username': username,
            'password': password,
            'confirm_password': confirm_password
        }
        response = api_client.post(path=url, data=data)
        response_code = response.status_code
        assert response_code == status_code

        if response_code == HTTP_201_CREATED:
            assert response.data['detail'] == 'Your activation email sent to your inbox.'

