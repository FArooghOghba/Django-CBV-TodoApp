import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_200_OK, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
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
class TestAccountsAPITokenAuthentication:
    @pytest.mark.parametrize(
            'email, password, status_code, is_verified', [
                ('wrong_email', 'far!@#$%', HTTP_400_BAD_REQUEST, False),
                ('test_email@test.com', 'wrong_pass', HTTP_400_BAD_REQUEST, False),
                ('test_email@test.com', 'far!@#$%', HTTP_400_BAD_REQUEST, False),
                ('test_email@test.com', 'far!@#$%', HTTP_200_OK, True),
            ]
        )
    def test_token_login_view(
            self, api_client, test_user,
            email, password, status_code, is_verified
    ):
        test_user.is_verified = is_verified
        test_user.save()

        url = reverse('accounts:api-v1:token-login')
        data = {
            'email': email,
            'password': password
        }

        response = api_client.post(path=url, data=data)
        assert response.status_code == status_code

        if status_code == HTTP_200_OK:
            test_token = Token.objects.get(user=test_user)
            assert test_token.key == response.data['token']

    def test_token_logout_view(self, api_client, test_user):
        test_user.is_verified = True
        test_user.save()

        url = reverse('accounts:api-v1:token-login')
        data = {
            'email': 'test_email@test.com',
            'password': 'far!@#$%'
        }
        api_client.post(path=url, data=data)

        url = reverse('accounts:api-v1:token-logout')
        api_client.force_login(user=test_user)
        response = api_client.post(path=url)
        assert response.status_code == HTTP_204_NO_CONTENT

