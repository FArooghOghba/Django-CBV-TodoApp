from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView
)

from jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from rest_framework_simplejwt.tokens import RefreshToken

from mail_templated import EmailMessage
from decouple import config

from .utils import EmailThread
from .forms import UserCreationModelForm, AccountActivationResendForm


User = get_user_model()


# Create your views here.


# Account Register
class AccountsRegisterFormView(FormView):
    """
    A view for displaying a register form and rendering a template response.
    """

    form_class = UserCreationModelForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('task:list')

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL
        :param form: registration form
        :return: if form valid register user.
        """
        user_obj = form.save()
        if user_obj is not None:
            email = user_obj.email
            username = user_obj.username
            token = self.get_token_for_user(user_obj)

            activation_email = EmailMessage(
                'email/activation_account.tpl',
                {
                    'user': username,
                    'token': f'http://127.0.0.1:8000/accounts/activation/confirm/{token}/',
                },
                'sender@example.com',
                [email]
            )
            EmailThread(activation_email).start()
            return HttpResponseRedirect(reverse_lazy('accounts:activation_send'))

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


# Account Activation Confirm
class AccountActivationConfirmTemplateView(TemplateView):
    """
    Confirm Activation view to activate user account.
    This view should be accessible for authenticated users.
    """
    template_name = 'accounts/account-activation-confirm.html'

    def get(self, request, *args, **kwargs):
        context = {}
        token = kwargs.get('token')
        try:
            decoded_token = decode(jwt=token, key=config('SECRET_KEY'), algorithms=['HS256'])
            user_id = decoded_token.get('user_id')
            user = User.objects.get(pk=user_id)
            context["response"] = "Your account activated successfully."

            if user.is_verified:
                context["response"] = "Your account has already verified."

            user.is_verified = True
            user.save()

        except ExpiredSignatureError:
            context["response"] = "Your token has been expired."
        except InvalidSignatureError:
            context["response"] = "Your token is not valid."

        return render(request, template_name=self.template_name, context=context)


# Account Activation Email Send
class AccountsActivationEmailSendTemplateView(TemplateView):
    """
    Render a template.
    """
    template_name = 'accounts/account-activation-send.html'


# Account Activation Resend
class AccountActivationEmailResendFormView(FormView):
    """
    A view for displaying a resend activation email form and
    rendering a template response.
    """
    form_class = AccountActivationResendForm
    template_name = 'accounts/account-activation-resend.html'
    success_url = reverse_lazy('accounts:activation_send')

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL
        :param form: resend activation email form
        :return: if form valid resend email.
        """
        email = form.cleaned_data['email']

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            form.add_error(
                field='email',
                error='Enter your email that you register with it.'
            )
            return super(AccountActivationEmailResendFormView, self).form_invalid(form)

        token = self.get_token_for_user(user_obj)
        username = user_obj.username
        activation_email = EmailMessage(
            'email/activation_account.tpl',
            {
                'user': username,
                'token': f'http://127.0.0.1:8000/accounts/activation/confirm/{token}/',
            },
            'sender@example.com',
            [email]
        )

        EmailThread(activation_email).start()

        return super(AccountActivationEmailResendFormView, self).form_valid(form)


# Accounts Password Change
class AccountsPasswordChangeView(PasswordChangeView):
    """
    A view for displaying a change password form and
    rendering a template response.
    """
    template_name = 'accounts/change-password.html'
    success_url = reverse_lazy('accounts:password_change_done')


# Account Password Change Done
class AccountsPasswordChangeDoneView(PasswordChangeDoneView):
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    """
    template_name = 'accounts/change-password-done.html'


# Account Login
class AccountsLoginView(LoginView):
    """
    Display the login form and handle the login action.
    """

    template_name = 'accounts/login.html'
    fields = ('email', 'password')
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task:list')

    def form_valid(self, form):
        """
        If the form is valid, checks for user is verified or not
        :param form: login form
        :return: logged-in user if user is verified or
        going back to log-in form with error.
        """
        user = form.get_user()
        if not user.is_verified:
            return HttpResponseRedirect(
                reverse_lazy('accounts:activation_resend'))
            # form.add_error(
            #     field=None,
            #     error='You are not verified your account yet.'
            # )
            # return super(AccountsLoginView, self).form_invalid(form)

        return super(AccountsLoginView, self).form_valid(form)


# Account Logout
class AccountsLogoutView(LogoutView):
    """
    Log out the user and display
    the 'You are logged out' message.
    """
    next_page = reverse_lazy('accounts:login')
