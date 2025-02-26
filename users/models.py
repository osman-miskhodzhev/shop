from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя
    Дополнительные поля:
        Изображение профиля
        Имя
        Фамилия
    """
    profile_image = models.ImageField(
        verbose_name='Фото профиля',
        upload_to='users/',
        default='users/baselogo.jpg'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=120,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=120,
    )
    is_verified_email = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    class Meta:
        verbose_name = 'Верификация через почту'
        verbose_name_plural = 'Верефикации через почту'

    def __str__(self):
        return f'EmailVerification obj for {self.user.email}'
    
    def send_verification_mail(self):
        link = reverse(
            'users:verify',
            kwargs={
                'email': self.user.email,
                'code': self.code
            }
        )
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        send_mail(
            'Subject',
            f'Подтверждение почты - {verification_link}',
            settings.EMAIL_HOST_USER,
            [self.user.email],
            fail_silently=False,

        )
    
    def is_expired(self):
        return True if now() >= self.expiration else False
