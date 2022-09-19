from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=50,
                                verbose_name='Имя пользователя',
                                unique=True)
    email = models.EmailField(max_length=250,
                              verbose_name='Электронная почта',
                              unique=True)
    first_name = models.CharField(max_length=50,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=50,
                                 verbose_name='Фамилия')
    bio = models.TextField(max_length=500,
                           verbose_name='О себе',
                           blank=True,
                           null=True)
    is_staff = models.BooleanField(default=False,
                                   verbose_name='Статус админа')

    REQUIRED_FIELDS = ['password', 'email',
                       'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
