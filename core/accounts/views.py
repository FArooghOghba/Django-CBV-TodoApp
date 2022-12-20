from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView
)

from .forms import UserCreationForm


# Create your views here.

class AccountsRegisterFormView(FormView):
    """
    A view for displaying a register form and rendering a template response.
    """

    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('task:list')

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL
        :param form: registration form
        :return: if form valid register user.
        """
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(AccountsRegisterFormView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests: instantiate a blank version of the form.
        :param request: self.user
        :param args:
        :param kwargs:
        :return:
        """

        if self.request.user.is_authenticated:
            return redirect('task:list')
        return super(AccountsRegisterFormView, self).get(request, *args, **kwargs)


class AccountsPasswordChangeView(PasswordChangeView):
    """
    A view for displaying a change password form and
    rendering a template response.
    """
    template_name = 'accounts/change-password.html'
    success_url = reverse_lazy('accounts:password_change_done')


class AccountsPasswordChangeDoneView(PasswordChangeDoneView):
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    """
    template_name = 'accounts/change-password-done.html'

class AccountsLoginView(LoginView):
    """
    Display the login form and handle the login action.
    """

    template_name = 'accounts/login.html'
    fields = ('email', 'password')
    redirect_authenticated_user = True

    def form_valid(self, form):
        """
        If the form is valid, checks for user is verified or not
        :param form: login form
        :return: logged-in user if user is verified or
        going back to log-in form with error.
        """
        user = form.get_user()
        if not user.is_verified:
            form.add_error(
                field=None,
                error='You are not verified your account yet.'
            )
            return super(AccountsLoginView, self).form_invalid(form)

        return super(AccountsLoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task:list')


class AccountsLogoutView(LogoutView):
    """
    Log out the user and display
    the 'You are logged out' message.
    """
    next_page = reverse_lazy('accounts:login')
