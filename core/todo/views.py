from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .models import Task
from .forms import TaskForm


# Create your views here.

class TaskListView(ListView):
    """
    Render some Task list of objects, set by `self.model`.
    """

    model = Task
    context_object_name = 'tasks'


class TaskCreateView(CreateView):
    """
    View for creating a new Task object, with a response
    rendered by a template.
    """

    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)
