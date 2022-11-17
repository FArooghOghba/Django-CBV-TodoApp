from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
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


class TaskDetailView(LoginRequiredMixin, DetailView):
    """
    Render a "detail" view of a task object.

    By default, this is a model instance looked up from `self.queryset`, but the
    view will support display of *any* object by overriding `self.get_object()`.
    """

    model = Task
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.
        This method is called by the default implementation of get_object() and
        may not be called if function get_object() is overridden.
        :return: user task
        """

        return self.model.objects.filter(user=self.request.user)


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

    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.
        This method is called by the default implementation of get_object() and
        may not be called if function get_object() is overridden.
        :return: user task
        """

        return self.model.objects.filter(user=self.request.user)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a task object retrieved with self.get_object(), with a
    response rendered by a template.
    """

    model = Task
    pk_url_kwarg = 'task_id'
    context_object_name = 'task'
    success_url = reverse_lazy('task:list')

    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.
        This method is called by the default implementation of get_object() and
        may not be called if function get_object() is overridden.
        :return: user task
        """

        return self.model.objects.filter(user=self.request.user)


class TaskCompleteView(View):
    model = Task
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('task:list')

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.get('task_id'))

        if task.complete:
            task.complete = False
        else:
            task.complete = True

        task.save()
        return redirect('task:list')
