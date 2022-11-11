from django.forms import ModelForm

from .models import Status


class StatusCreationForm(ModelForm):
    """Form for creating a status."""

    class Meta:
        model = Status
        fields = ("name",)
