from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, LoginForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # ADD MESSAGE Пользователь успешно зарегистрирован
            return redirect("login")
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # ADD MESSAGE Вы залогинены
                    return redirect('home')
                else:
                    # ADD MESSAGE Ваш аккаунт неактивен
                    return redirect("login")
            else:
                # ADD MESSAGE Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.
                return redirect("login")
    else:
        form = LoginForm()
    return render(request, 'pages/login.html', {'form': form})


def logout_user(request):
    if request.method == "POST":
        logout(request)
    # ADD MESSAGE Вы разлогинены
    return redirect("home")


def users(request):
    all_users = User.objects.order_by('date_joined')
    return render(request, 'accounts/users.html', {'all_users': all_users})