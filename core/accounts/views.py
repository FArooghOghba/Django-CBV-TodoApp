from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = ('email', 'password')
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task:list')
