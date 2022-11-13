from django.forms import ModelForm

from .models import Tag


class TagCreationForm(ModelForm):
    """Form for creating a tag."""

    class Meta:
        model = Tag
        fields = ("name",)
