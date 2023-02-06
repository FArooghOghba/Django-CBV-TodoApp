from datetime import datetime
import requests

from django.core.cache import cache
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm


city_name = 'Ahvaz'
api_key = 'a2fa7b56cab242ab3dbc85164885ca3b'
units = 'metric'
open_weather_url = f"https://api.openweathermap.org/data/2.5/weather?" \
                   f"q={city_name}&appid={api_key}&units={units}"


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
        task_count = context['tasks'].filter(complete=False).count()
        context['incomplete_task_count'] = task_count

        search = self.request.GET.get('search', '')
        if search:
            context['tasks'] = context['tasks'].filter(title__icontains=search)
        context['search'] = search

        # getting weather from openweather api
        if cache.get('weather') is None:
            response = requests.get(url=open_weather_url)
            cache.set('weather', response.json(), 60 * 20)

        context['weather_description'] = cache.get('weather')['weather'][0]['description']
        context['temp'] = cache.get('weather')['main']['temp']

        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    """
    Render a "detail" view of a task object.

    By default, this is a model instance looked up
    from `self.queryset`, but the view will support
    display of *any* object by overriding `self.get_object()`.
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
    """
    View for checking a task object as complete and doesn't need to use
    edit page.
    """

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
