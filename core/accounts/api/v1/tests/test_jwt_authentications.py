import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK, HTTP_401_UNAUTHORIZED
)


User = get_user_model()


@pytest.fixture
def api_client():
   return APIClient()


@pytest.fixture
def test_user():
    user = User.objects.create_user(
        email='test_email@test.com',
        username='test_username',
        password='far!@#$%'
    )
    return user


@pytest.mark.django_db
class TestAccountsJWTAuthentication:
    @pytest.mark.parametrize(
            'email, password, is_verified, status_code', [
                ('wrong_email', 'far!@#$%', False, HTTP_401_UNAUTHORIZED),
                ('test_email@test.com', 'wrong_pass', False, HTTP_401_UNAUTHORIZED),
                ('test_email@test.com', 'far!@#$%', False, HTTP_401_UNAUTHORIZED),
                ('test_email@test.com', 'far!@#$%', True, HTTP_200_OK),
            ]
        )
    def test_token_obtain_pair_view(
            self, api_client, test_user,
            email, password, is_verified, status_code
    ):
        test_user.is_verified = is_verified
        test_user.save()

        url = reverse('accounts:api-v1:jwt-create')
        data = {
            'email': email,
            'password': password
        }

        response = api_client.post(path=url, data=data)
        assert response.status_code == status_code
        print(response.data)
