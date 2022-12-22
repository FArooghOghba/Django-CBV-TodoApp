from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


# Getting User Model

user = get_user_model()


class UserCreationModelForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)

    class Meta:
        model = user
        fields = ('email', 'username', 'password1', 'password2')


class AccountActivationResendForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True)

