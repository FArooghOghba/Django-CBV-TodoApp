from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView

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
        If the form is valid, redirect to the supplied URL.
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


class AccountsLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = ('email', 'password')
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task:list')


class AccountsLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')
