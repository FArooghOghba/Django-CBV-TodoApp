from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm


# Getting User Model

user = get_user_model()


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(max_length=255, required=True)

    class Meta:
        model = user
        fields = ('email', 'username', 'password1', 'password2')
