from django.urls import path

from . import views

urlpatterns = [
    path("", views.TagListView.as_view(), name="tags"),
    path("create/", views.TagCreateView.as_view(), name="create_tag"),
    path(
        "<int:pk>/update/",
        views.TagUpdateView.as_view(),
        name="update_tag",
    ),
    path(
        "<int:pk>/delete/",
        views.TagDeleteView.as_view(),
        name="delete_tag",
    ),
]
