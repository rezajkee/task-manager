from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from ..utils import CustomLoginRequiredMixin
from .forms import StatusCreationForm
from .models import Status


class StatusCreateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, generic.CreateView
):
    """Status creation only by logged in user
    with adding a success message."""

    form_class = StatusCreationForm
    success_url = reverse_lazy("statuses")
    template_name = "statuses/create_status.html"
    success_message = _("StatusCreateSuccessMessage")


class StatusListView(CustomLoginRequiredMixin, generic.ListView):
    """Render list of all existing statuses only by logged in user."""

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
    """Updating status's name only by logged in user
    and add a success message."""

    model = Status
    form_class = StatusCreationForm
    template_name = "statuses/update_status.html"
    success_url = reverse_lazy("statuses")
    success_message = _("StatusUpdateSuccessMessage")


class StatusDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Delete status only by logged in user
    and add a success message."""

    model = Status
    template_name = "statuses/delete_status.html"
    success_url = reverse_lazy("statuses")
    success_message = _("StatusDeleteSuccessMessage")
