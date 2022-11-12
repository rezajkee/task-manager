from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from ..utils import CustomLoginRequiredMixin, CustomUserPassesTestMixin
from .forms import TaskCreationForm
from .models import Task


class TasksUserPassesTestMixin(CustomUserPassesTestMixin):
    """Override mixin attributes for a tasks views."""

    permission_denied_message = _("TasksUserPassesMessage")
    redirect_url = "tasks"


class TaskCreateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, generic.CreateView
):
    """Task creation only by a logged-in user
    with adding this user as the author and
    adding the success message."""

    form_class = TaskCreationForm
    success_url = reverse_lazy("tasks")
    template_name = "tasks/create_task.html"
    success_message = _("TaskCreateSuccessMessage")

    def form_valid(self, form):
        # Add logged-in user as the author
        form.instance.author = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskListView(CustomLoginRequiredMixin, generic.ListView):
    """Rendering a list of all existing tasks only by a logged-in user."""

    model = Task
    fields = ("id", "name", "creation_date")
    context_object_name = "all_tasks"
    ordering = ["creation_date"]
    template_name = "tasks/tasks.html"


class TaskUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Updating task's fields only by a logged-in user
    with adding the success message."""

    model = Task
    form_class = TaskCreationForm
    template_name = "tasks/update_task.html"
    success_url = reverse_lazy("tasks")
    success_message = _("TaskUpdateSuccessMessage")


class TaskDeleteView(
    CustomLoginRequiredMixin,
    TasksUserPassesTestMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Deleting a task only by the author
    with adding the success message."""

    model = Task
    template_name = "tasks/delete_task.html"
    success_url = reverse_lazy("tasks")
    success_message = _("TaskDeleteSuccessMessage")

    def test_func(self):
        return self.request.user.id == self.kwargs["pk"]


class TaskDetailView(
    CustomLoginRequiredMixin,
    generic.DetailView,
):
    """Rendering a page of the detailed task only by a logged-in user."""
    model = Task
    template_name = "tasks/detail_task.html"
