from django.db import models
from django.contrib.auth import get_user_model


# Get user model

user = get_user_model()


# Create your models here.

class Task(models.Model):
    """
    This is a model class to define tasks for todoapp.
    """

    user = models.ForeignKey(user, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    descriptions = models.TextField()
    complete = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']

