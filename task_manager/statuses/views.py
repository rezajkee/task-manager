from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from ..utils import CustomLoginRequiredMixin
from .forms import StatusCreationForm
from .models import Status


class StatusCreateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, generic.CreateView
):
    """Status creation only by a logged-in user
    with adding the success message."""

    form_class = StatusCreationForm
    success_url = reverse_lazy("statuses")
    template_name = "statuses/create_status.html"
    success_message = _("The status was created successfully")


class StatusListView(CustomLoginRequiredMixin, generic.ListView):
    """Rendering a list of all existing statuses only by a logged-in user."""

    model = Status
    fields = ("id", "name", "creation_date")
    context_object_name = "all_statuses"
    ordering = ["creation_date"]
    template_name = "statuses/statuses.html"


class StatusUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Updating status's name only by a logged-in user
    with adding the success message."""

    model = Status
    form_class = StatusCreationForm
    template_name = "statuses/update_status.html"
    success_url = reverse_lazy("statuses")
    success_message = _("The status was edited successfully")


class StatusDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Deleting a status only by a logged-in user
    with adding the success message.
    Prohibit deletion if status
    involved in a task."""

    model = Status
    template_name = "statuses/delete_status.html"
    success_url = reverse_lazy("statuses")
    success_message = _("The status was deleted successfully")

    def post(self, request, *args, **kwargs):
        try:
            return super(StatusDeleteView, self).post(
                self, request, *args, **kwargs
            )
        except ProtectedError:
            messages.add_message(
                request,
                messages.ERROR,
                _(
                    """It is not possible to delete the
                    status because it is being used"""
                ),
            )
            return redirect("statuses")
