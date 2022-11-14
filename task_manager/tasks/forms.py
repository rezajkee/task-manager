from django.forms import ModelForm

from .models import Task


class TaskCreationForm(ModelForm):
    """Form for creating a task."""

    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
