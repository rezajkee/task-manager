from django.urls import path
from task_manager.accounts import views

urlpatterns = [
    path('', views.users, name='users'),
    path('create/', views.register, name='register'),
]
