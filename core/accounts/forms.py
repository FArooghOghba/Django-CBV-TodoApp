from django import forms

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Getting User Model

user = get_user_model()


class UserCreationModelForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)

    class Meta:
        model = user
        fields = ('email', 'username', 'password1', 'password2')


class AccountActivationResendForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True)


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(required=False)
    email = forms.EmailField(max_length=255, required=True)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
