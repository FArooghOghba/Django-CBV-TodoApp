import pytest
from pytest_django.asserts import assertRedirects

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.status import (
    HTTP_302_FOUND, HTTP_200_OK, HTTP_401_UNAUTHORIZED
)
from time import sleep

from ..forms import CustomAuthenticationForm


User = get_user_model()


@pytest.fixture
def test_user():
    user = User.objects.create_user(
        email='user_testemail@test.com',
        username='test_username',
        password='far!@#$%'
    )
    return user

@pytest.mark.django_db
class TestAccountsRegistrationViews:

    def test_accounts_register_view(self, client, mailoutbox):
        url = reverse('accounts:register')
        data = {
            'email': 'test_register@test.com',
            'username': 'test_username_register',
            'password1': 'password2register',
            'password2': 'password2register',
        }
        response = client.post(url, data)
        assert response.status_code == HTTP_302_FOUND

        sleep(1)
        print(mailoutbox)
        assert len(mailoutbox) == 1
        email = mailoutbox[0]
        assert email.subject == 'Email Verification'

    def test_accounts_activation_resend_view(self, client, test_user, mailoutbox):

        url = reverse('accounts:activation_resend')
        data = {
            'email': test_user.email,
        }
        response = client.post(path=url, data=data)
        assert response.status_code == HTTP_302_FOUND

        sleep(1)
        print(mailoutbox)
        assert len(mailoutbox) == 1
        email = mailoutbox[0]
        assert email.subject == 'Email Verification'


@pytest.mark.django_db
class TestAccountsAuthenticationView:

    @pytest.mark.parametrize(
        'expected_url, user_is_verified', [
            ('accounts:activation_resend', False),
            ('task:list', True),
        ]
    )
    def test_accounts_login_http_200_ok(
            self, client, test_user, expected_url,
            user_is_verified
    ):

        url = reverse('accounts:login')
        data = {
            'email': test_user.email,
            'password': 'far!@#$%'
        }

        test_user.is_verified = user_is_verified
        test_user.save()

        response = client.post(url, data)
        assertRedirects(
            response, expected_url=reverse(expected_url),
            status_code=HTTP_302_FOUND, target_status_code=HTTP_200_OK
        )

    @pytest.mark.parametrize(
        'email, password', [
            ('', ''),
            ('user_testemail@test.com', 'wrong_pass'),
            ('user@example.com', ''),
            ('', 'far!@#$%'),
            ('wrong.email@example.com', 'far!@#$%'),
        ]
    )
    def test_accounts_login_http_401_unauthorized(
            self, client, test_user, email, password
    ):
        url = reverse('accounts:login')
        data = {
            'email': email,
            'password': password
        }

        response = client.post(url, data)
        assert response.status_code == HTTP_401_UNAUTHORIZED