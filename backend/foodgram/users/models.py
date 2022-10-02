from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150,
                                verbose_name='Имя пользователя',
                                unique=True,
                                blank=False
                                )
    email = models.EmailField(max_length=254,
                              verbose_name='Электронная почта',
                              unique=True,
                              blank=False
                              )
    first_name = models.CharField(max_length=150,
                                  verbose_name='Имя',
                                  blank=False
                                  )
    last_name = models.CharField(max_length=150,
                                 verbose_name='Фамилия',
                                 blank=False
                                 )
    is_staff = models.BooleanField(default=False,
                                   verbose_name='Статус админа'
                                   )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def set_to_admin(self):
        self.is_staff = True

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    follower = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='following',
                                 verbose_name='Подписчик')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='followed',
                               verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        constraints = [models.UniqueConstraint(fields=['follower', 'author'],
                                               name='unique_subscribe'
                                               )
                       ]

    def __str__(self):
        return f'Подписка на {self.author}'
