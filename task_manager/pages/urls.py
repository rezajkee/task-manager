from django.urls import path
from django.views.generic.base import TemplateView
from task_manager.accounts import views as acc_views

urlpatterns = [
    path(
        "", TemplateView.as_view(template_name="pages/home.html"), name="home"
    ),
    path("login/", acc_views.CustomLoginView.as_view(), name="login"),
    path("logout/", acc_views.CustomLogoutView.as_view(), name="logout"),
]
