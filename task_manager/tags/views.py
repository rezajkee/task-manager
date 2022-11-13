from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from ..utils import CustomLoginRequiredMixin
from .forms import TagCreationForm
from .models import Tag


class TagCreateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, generic.CreateView
):
    """Tag creation only by a logged-in user
    with adding the success message."""

    form_class = TagCreationForm
    success_url = reverse_lazy("tags")
    template_name = "tags/create_tag.html"
    success_message = _("TagCreateSuccessMessage")


class TagListView(CustomLoginRequiredMixin, generic.ListView):
    """Rendering a list of all existing tags only by a logged-in user."""

    model = Tag
    fields = ("id", "name", "creation_date")
    context_object_name = "all_tags"
    ordering = ["creation_date"]
    template_name = "tags/tags.html"


class TagUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Updating tag's name only by a logged-in user
    with adding the success message."""

    model = Tag
    form_class = TagCreationForm
    template_name = "tags/update_tag.html"
    success_url = reverse_lazy("tags")
    success_message = _("TagUpdateSuccessMessage")


class TagDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Deleting a tag only by a logged-in user
    with adding the success message.
    Prohibit deletion if tag
    involved in a task."""

    model = Tag
    template_name = "tags/delete_tag.html"
    success_url = reverse_lazy("tags")
    success_message = _("TagDeleteSuccessMessage")

    def post(self, request, *args, **kwargs):
        try:
            return super(TagDeleteView, self).post(
                self, request, *args, **kwargs
            )
        except ProtectedError:
            messages.add_message(
                request, messages.ERROR, _("TagProtectedMessage")
            )
            return redirect("tags")
