import pytest

from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
class TestAccountsModels:
    data = {
      'email': 'test@email_test.com',
      'username': 'test_username',
      'password': 'test_password'
    }

    def test_accounts_model_create_user(self):
        test_user = User.objects.create_user(**self.data)
        assert User.objects.count() == 1
        assert test_user.is_superuser is False

    def test_accounts_model_create_superuser(self):
        test_user = User.objects.create_superuser(**self.data)
        assert User.objects.count() == 1
        assert test_user.is_superuser is True
