from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from ..utils import CustomLoginRequiredMixin
from .forms import LabelCreationForm
from .models import Label


class LabelCreateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, generic.CreateView
):
    """Label creation only by a logged-in user
    with adding the success message."""

    form_class = LabelCreationForm
    success_url = reverse_lazy("labels")
    template_name = "labels/create_label.html"
    success_message = _("The label was created successfully")


class LabelListView(CustomLoginRequiredMixin, generic.ListView):
    """Rendering a list of all existing labels only by a logged-in user."""

    model = Label
    fields = ("id", "name", "creation_date")
    context_object_name = "all_labels"
    ordering = ["creation_date"]
    template_name = "labels/labels.html"


class LabelUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Updating label's name only by a logged-in user
    with adding the success message."""

    model = Label
    form_class = LabelCreationForm
    template_name = "labels/update_label.html"
    success_url = reverse_lazy("labels")
    success_message = _("The label was edited successfully")


class LabelDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Deleting a label only by a logged-in user
    with adding the success message.
    Prohibit deletion if label
    involved in a task."""

    model = Label
    template_name = "labels/delete_label.html"
    success_url = reverse_lazy("labels")
    success_message = _("The label was deleted successfully")

    def post(self, request, *args, **kwargs):
        try:
            return super(LabelDeleteView, self).post(
                self, request, *args, **kwargs
            )
        except ProtectedError:
            messages.add_message(
                request, messages.ERROR, _("It is not possible to delete the label because it is being used")
            )
            return redirect("labels")
