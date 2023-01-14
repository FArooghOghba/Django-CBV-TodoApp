import pytest

from time import sleep

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_202_ACCEPTED, HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)
from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage

from ....utils import EmailThread

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
class TestPasswordManagements:

    domain = 'http://127.0.0.1:8000/'

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def send_activation_email(self, token, user):
        email = user.email
        username = user.username
        urls = 'accounts/api/v1/reset_password/confirm/'

        activation_email = EmailMessage(
            template_name='email/reset_password.tpl',
            context={
                'user': username,
                'token': f'{self.domain}{urls}{token}/',
            },
            from_email='sender@example.com',
            to=[email]
        )
        EmailThread(activation_email).start()

    @pytest.mark.parametrize(
        'old_password, new_password, confirm_new_password, status_code', [
            ('far!@#$%', 'far123123', 'far123123', HTTP_202_ACCEPTED),
            ('wrong_pass', 'far123123', 'far123123', HTTP_400_BAD_REQUEST),
            ('far!@#$%', 'far123123', 'wrong_pass', HTTP_400_BAD_REQUEST),
        ]
    )
    def test_change_password_view(
            self, api_client, test_user, status_code,
            old_password, new_password, confirm_new_password
    ):
        api_client.force_login(test_user)

        url = reverse('accounts:api-v1:change-password')
        data = {
            'old_password': old_password,
            'new_password': new_password,
            'confirm_new_password': confirm_new_password
        }
        response = api_client.put(path=url, data=data)

        assert response.status_code == status_code


    def test_reset_password_view(
            self, api_client, test_user, mailoutbox
    ):

        url = reverse(
            'accounts:api-v1:reset_password',
        )

        data = {
            'email': 'test_email@test.com'
        }

        api_client.force_login(test_user)
        response = api_client.post(path=url, data=data)

        sleep(1)
        assert response.status_code == HTTP_200_OK

        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        assert mail.subject == 'Reset Password'
        assert list(mail.to) == [test_user.email]


    def test_reset_password_confirm_view(
            self, api_client, test_user, mailoutbox
    ):

        token = self.get_token_for_user(test_user)
        self.send_activation_email(token, test_user)

        url = reverse(
            'accounts:api-v1:reset_password_confirm',
            kwargs={'token': token}
        )
        data = {
            'new_password': 'far123123',
            'confirm_new_password': 'far123123'
        }
        response = api_client.put(path=url, data=data)

        # check token
        assert response.status_code == HTTP_202_ACCEPTED
        assert mailoutbox[0].context['token'] == f'http://127.0.0.1:8000{url}'

