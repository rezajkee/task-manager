from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from .forms import UserRegistrationForm
from .utils import (
    CustomLoginRequiredMixin,
    CustomUserPassesTestMixin,
    PlaceholderMixin,
)


class CustomAuthenticationForm(PlaceholderMixin, AuthenticationForm):
    """Add placeholders and 'form-control' class to
    AuthenticationForm fields."""

    pass


class CustomLoginView(SuccessMessageMixin, LoginView):
    """Override authentication form to CustomAuthenticationForm,
    change template path, add success message after authentication."""

    template_name = "pages/login.html"
    authentication_form = CustomAuthenticationForm
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
    CustomUserPassesTestMixin,
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
    CustomUserPassesTestMixin,
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


# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user = user_form.save(commit=False)
#             new_user.set_password(user_form.cleaned_data['password'])
#             new_user.save()
#             # ADD MESSAGE Пользователь успешно зарегистрирован
#             return redirect("login")
#     else:
#         user_form = UserRegistrationForm()
#     return render(request, 'accounts/register.html', {'user_form': user_form})


# def login_user(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(
#                               username=cd['username'], password=cd['password']
#             )
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     messages.add_message(request, messages.SUCCESS,
#                                         _('LoginSuccessMessage'))
#                     return redirect('home')
#                 else:
#                     messages.add_message(request, messages.ERROR,
#                                         _('InactiveAccountMessage'))
#                     # ADD MESSAGE Ваш аккаунт неактивен
#                     return redirect("login")
#             else:
#                 messages.add_message(request, messages.ERROR,
#                                     _('WrongLoginMessage'))
#                 # ADD MESSAGE Пожалуйста, введите правильные
#                 return redirect("login")
#     else:
#         form = LoginForm()
#     return render(request, 'pages/login.html', {'form': form})


# def logout_user(request):
#     if request.method == "POST":
#         logout(request)
#     messages.add_message(request, messages.SUCCESS,
#                         _('LogoutSuccessMessage'))
#     return redirect("home")


# def users(request):
#     all_users = User.objects.order_by('date_joined')
#     return render(request, 'accounts/users.html', {'all_users': all_users})
