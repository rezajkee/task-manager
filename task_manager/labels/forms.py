from django.forms import ModelForm

from .models import Label


class LabelCreationForm(ModelForm):
    """Form for creating a label."""

    class Meta:
        model = Label
        fields = ("name",)
