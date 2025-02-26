from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy, reverse

from .forms import (
    CustomAuthenticationForm,
    CustomUserForm,
    UserRegistrationForm
)
from .models import CustomUser, EmailVerification
from products.models import Basket


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
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context


class UserUpdate(UpdateView):
    """Представление для обработки обновлений данных о пользователе"""
    model = CustomUser
    form_class = CustomUserForm

    template_name = 'users/profile.html'

    success_url = reverse_lazy('users:profile')

class EmailVerificationView(TemplateView):
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = CustomUser.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(code=code, user=user)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
        else:
            return HttpResponseRedirect(reverse('users:index'))
        return super(EmailVerificationView, self).get(request, *args, **kwargs)
