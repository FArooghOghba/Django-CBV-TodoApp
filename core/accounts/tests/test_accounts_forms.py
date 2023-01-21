import pytest

from django.contrib.auth import get_user_model
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
class TestAccountsAuthenticationView2:

    def test_login_view(self, test_user):
        print(test_user.email)

        data = {
            'email': test_user.email,
            'password': 'far!@#$%'
        }

        form = CustomAuthenticationForm(data=data)

        assert form.is_valid() is True
