from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """The LoginRequiredMixin extended to add a relevant message to the
    messages framework by setting the 'login_required_message'
    attribute."""

    login_required_message = _("LoginRequiredMessage")
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
    page without raising the PermissionDenied exception."""

    permission_denied_message = _("UserPassesMessage")

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            messages.add_message(
                request, messages.ERROR, self.permission_denied_message
            )
            return redirect("users")
        return super(CustomUserPassesTestMixin, self).dispatch(
            request, *args, **kwargs
        )
