from django.forms import ModelForm

from ..utils import PlaceholderMixin
from .models import Status


class StatusCreationForm(PlaceholderMixin, ModelForm):
    """Form with adding a placeholders and 'form-control' class."""

    class Meta:
        model = Status
        fields = ("name",)
