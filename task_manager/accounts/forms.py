from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _

from ..utils import PlaceholderMixin


class UserRegistrationForm(PlaceholderMixin, UserCreationForm):
    """Add placeholders and 'form-control' class to
    UserCreationForm fields."""

    first_name = forms.CharField(label=_("FirstNameTitle"), max_length=50)
    last_name = forms.CharField(label=_("LastNameTitle"), max_length=50)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")


class CustomAuthenticationForm(PlaceholderMixin, AuthenticationForm):
    """Add placeholders and 'form-control' class to
    AuthenticationForm fields."""

    pass
