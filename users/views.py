from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy

from .forms import (
    CustomAuthenticationForm,
    CustomUserForm,
    UserRegistrationForm
)
from .models import CustomUser


class UserRegistration(CreateView):
    template_name = 'registration/registration.html'
    model = CustomUser
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')


class CustomLoginView(LoginView):
    """
    Кастомное представление страницы авторизации
    Передает форму авторизации
    """
    form_class = CustomAuthenticationForm


class ProfileView(TemplateView):
    """
    Представление профиля
    Передает форму для работы со данными о пользователе
    """
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        """Метод формирования контекста"""
        context = super().get_context_data(**kwargs)
        context['form'] = CustomUserForm
        return context


class UserUpdate(UpdateView):
    """Представление для обработки обновлений данных о пользователе"""
    model = CustomUser
    form_class = CustomUserForm

    template_name = 'users/profile.html'

    success_url = reverse_lazy('users:profile')
