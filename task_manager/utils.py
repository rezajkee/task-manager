from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """The LoginRequiredMixin extended to add a relevant message to the
    messages framework by setting the 'login_required_message'
    attribute."""

    login_required_message = _("You are not logged in! Please log in.")
    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.ERROR, self.login_required_message
            )
            return self.handle_no_permission()
        return super(CustomLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )


class CustomUserPassesTestMixin(UserPassesTestMixin):
    """Override UserPassesTestMixin method 'dispatch' to add
    a relevant message to the messages framework by setting the
    'permission_denied_message' attribute and redirect to users
    page without raising the PermissionDenied exception.
    Don't forget to override "permission_denied_message" and
    "redirect_url" attributes in CustomUserPassesTestMixin."""

    permission_denied_message = (
        "Don't forget to override attributes in CustomUserPassesTestMixin"
    )
    redirect_url = "home"

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            messages.add_message(
                request, messages.ERROR, self.permission_denied_message
            )
            return redirect(self.redirect_url)
        return super(CustomUserPassesTestMixin, self).dispatch(
            request, *args, **kwargs
        )
