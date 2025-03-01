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
from core.views import CommonTemplateMixin


class UserRegistration(CommonTemplateMixin, CreateView):
    template_name = 'registration/registration.html'
    title = 'Регистрация'
    model = CustomUser
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')


class CustomLoginView(CommonTemplateMixin, LoginView):
    """
    Кастомное представление страницы авторизации
    Передает форму авторизации
    """
    form_class = CustomAuthenticationForm
    title = 'Авторизация'


class ProfileView(CommonTemplateMixin, TemplateView):
    """
    Представление профиля
    Передает форму для работы со данными о пользователе
    """
    template_name = 'users/profile.html'
    title = 'Профиль'

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

    success_url = reverse_lazy('users:profile')


class EmailVerificationView(CommonTemplateMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Подтверждение почты'

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
