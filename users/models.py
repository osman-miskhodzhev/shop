from django.contrib.auth.models import AbstractUser
from django.db import models


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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
