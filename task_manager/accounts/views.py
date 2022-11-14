from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from ..utils import CustomLoginRequiredMixin, CustomUserPassesTestMixin
from .forms import UserRegistrationForm


class AccountsUserPassesTestMixin(CustomUserPassesTestMixin):
    """Override mixin's attributes for a accounts views."""

    permission_denied_message = _("You have no rights to change another user.")
    redirect_url = "users"


class CustomLoginView(SuccessMessageMixin, LoginView):
    """Change template path, add success message after authentication."""

    template_name = "pages/login.html"
    success_message = _("You are logged in")


class CustomLogoutView(LogoutView):
    """Override dispatch method to add success message after logout."""

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, _("You are logged out"))
        return super(CustomLogoutView, self).dispatch(request, *args, **kwargs)


class UserCreateView(SuccessMessageMixin, generic.CreateView):
    """User registration with custom fields order
    and adding the success message."""

    form_class = UserRegistrationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/register.html"
    success_message = _("The user has been registered successfully")


class UserListView(generic.ListView):
    """Render a list of all registered users."""

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
    """Updating user's fields only by a user's owner
    and adding the success message."""

    model = User
    form_class = UserRegistrationForm
    template_name = "accounts/update_user.html"
    success_url = reverse_lazy("users")
    success_message = _("The user has been edited successfully")

    def test_func(self):
        return self.request.user.id == self.kwargs["pk"]


class UserDeleteView(
    CustomLoginRequiredMixin,
    AccountsUserPassesTestMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Delete a user only by a user's owner
    and adding the success message.
    Prohibit deletion if user
    involved in a task."""

    model = User
    template_name = "accounts/delete_user.html"
    success_url = reverse_lazy("users")
    success_message = _("The user has been deleted successfully")

    def test_func(self):
        return self.request.user.id == self.kwargs["pk"]

    def post(self, request, *args, **kwargs):
        try:
            return super(UserDeleteView, self).post(
                self, request, *args, **kwargs
            )
        except ProtectedError:
            messages.add_message(
                request, messages.ERROR, _("It is not possible to delete the user because he is being used")
            )
            return redirect("users")
