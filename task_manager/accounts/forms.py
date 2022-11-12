from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    """Set first_name and last_name fields to required."""

    first_name = forms.CharField(label=_("FirstNameTitle"), max_length=50)
    last_name = forms.CharField(label=_("LastNameTitle"), max_length=50)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")
