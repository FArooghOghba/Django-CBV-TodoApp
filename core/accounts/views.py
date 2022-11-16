from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.

class AccountsLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = ('email', 'password')
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task:list')


class AccountsLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')
