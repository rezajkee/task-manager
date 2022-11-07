from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .utils import PlaceholderMixin


class UserRegistrationForm(PlaceholderMixin, UserCreationForm):
    """Add placeholders and 'form-control' class to
    UserCreationForm fields."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")
