from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from ..utils import CustomLoginRequiredMixin, CustomUserPassesTestMixin
from .forms import UserRegistrationForm


class AccountsUserPassesTestMixin(CustomUserPassesTestMixin):
    """Override mixin attributes for a accounts views."""

    permission_denied_message = _("AccountsUserPassesMessage")
    redirect_url = "users"


class CustomLoginView(SuccessMessageMixin, LoginView):
    """Change template path, add success message after authentication."""

    template_name = "pages/login.html"
    success_message = _("LoginSuccessMessage")


class CustomLogoutView(LogoutView):
    """Override dispatch method to add success message after logout."""

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, _("LogoutSuccessMessage"))
        return super(CustomLogoutView, self).dispatch(request, *args, **kwargs)


class UserCreateView(SuccessMessageMixin, generic.CreateView):
    """User registration with custom fields order
    and add a success message."""

    form_class = UserRegistrationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/register.html"
    success_message = _("UserCreateSuccessMessage")


class UserListView(generic.ListView):
    """Render list of all registered users."""

    model = User
    form_class = UserRegistrationForm
    context_object_name = "all_users"
    ordering = ["date_joined"]
    template_name = "accounts/users.html"


class UserUpdateView(
    CustomLoginRequiredMixin,
    AccountsUserPassesTestMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Updating user's fields only by user's owner
    and add a success message."""

    model = User
    form_class = UserRegistrationForm
    template_name = "accounts/update_user.html"
    success_url = reverse_lazy("users")
    success_message = _("UserUpdateSuccessMessage")

    def test_func(self):
        return self.request.user.id == self.kwargs["pk"]


class UserDeleteView(
    CustomLoginRequiredMixin,
    AccountsUserPassesTestMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Delete user only by user's owner
    and add a success message."""

    model = User
    template_name = "accounts/delete_user.html"
    success_url = reverse_lazy("users")
    success_message = _("UserDeleteSuccessMessage")

    def test_func(self):
        return self.request.user.id == self.kwargs["pk"]
