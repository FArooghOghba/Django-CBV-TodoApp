from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm


# Create your views here.

class TaskListView(LoginRequiredMixin, ListView):
    """
    Render some Task list of objects, set by `self.model`.
    """

    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.model.objects.filter(user=self.request.user)
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
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


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating a task object, with a response
    rendered by a template.
    """

    model = Task
    form_class = TaskForm
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('task:list')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a task object retrieved with self.get_object(), with a
    response rendered by a template.
    """

    model = Task
    pk_url_kwarg = 'task_id'
    context_object_name = 'task'
    success_url = reverse_lazy('task:list')
