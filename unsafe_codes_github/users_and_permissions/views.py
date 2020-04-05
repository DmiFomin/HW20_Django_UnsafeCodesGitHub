from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import RegistrationForm
from django.views.generic import CreateView, ListView
from .models import AdvancedUser
from django.urls import reverse_lazy


# Create your views here.
class UserLoginView(LoginView):
    template_name = 'users_and_permissions/login.html'


class RegistrationUserView(CreateView):
    model = AdvancedUser
    template_name = 'users_and_permissions/registration_user.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users_and_permissions:login')


# Восстановление пароля
class UserPasswordResetView(PasswordResetView):
    template_name = 'users_and_permissions/password_reset.html'
    email_template_name = "users_and_permissions/password_reset_email.html",
    success_url = reverse_lazy('users_and_permissions:password_reset_done')


class UserPasswordDoneView(PasswordResetView):
    template_name = 'users_and_permissions/password_reset_done.html'


class UserPasswordConfirmView(PasswordResetView):
    template_name = 'users_and_permissions/password_reset_confirm.html'
    #success_url = reverse_lazy('users_and_permissions:password_reset_complete')


class UserPasswordCompleteView(PasswordResetView):
    template_name = 'users_and_permissions/password_reset_complete.html'


# def recovery_password(request):
#     return render(request, 'users_and_permissions/recovery_password.html', context={})