from time import sleep

import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_401_UNAUTHORIZED,
    HTTP_202_ACCEPTED
)

from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken

from ....utils import EmailThread

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
            status_code, mailoutbox
    ):

        url = reverse('accounts:api-v1:register')
        data = {
            'email': email,
            'username': username,
            'password': password,
            'confirm_password': confirm_password
        }
        response = api_client.post(path=url, data=data)

        sleep(1)
        response_code = response.status_code
        assert response_code == status_code

        if response_code == HTTP_201_CREATED:
            assert response.data['detail'] == 'Your activation email sent to your inbox.'

            assert len(mailoutbox) == 1
            mail = mailoutbox[0]
            assert mail.subject == 'Email Verification'
            assert list(mail.to) == [email]

    def test_accounts_api_activation_confirm_view(self, api_client, mailoutbox):
        test_user = User.objects.create_user(
            email='test_email@test.com',
            username='test_username',
            password='far!@#$%'
        )

        email = 'test_email@test.com'
        username = 'test_username'
        user_obj = test_user

        def get_token_for_user(user):
            refresh = RefreshToken.for_user(user)
            return str(refresh.access_token)

        token = get_token_for_user(user_obj)
        domain = 'http://127.0.0.1:8000/'
        urls = 'accounts/api/v1/activation/confirm/'

        activation_email = EmailMessage(
            template_name='email/activation_account.tpl',
            context={
                'user': username,
                'token': f'{domain}{urls}{token}/',
            },
            from_email='sender@example.com',
            to=[email]
        )

        EmailThread(activation_email).start()

        url = reverse(
            'accounts:api-v1:activation-confirm', kwargs={'token': token}
        )
        response = api_client.get(path=url)

        assert mailoutbox[0].context['token'] == f'http://127.0.0.1:8000{url}'
        assert response.status_code == HTTP_202_ACCEPTED
