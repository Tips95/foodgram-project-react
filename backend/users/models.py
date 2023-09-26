from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Класс, представляющий роли пользователей.
    """
    email = models.EmailField(
        unique=True
    )
    username = models.CharField(
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)


class Subscribe(models.Model):
    subscriber = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='подписчик',
        related_name='subscribers'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        related_name='authors',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('subscriber', 'author'),
                name='%(app_label)s_%(class)s_name_unique',
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F('subscriber')),
                name='%(app_label)s_%(class)s_self_sub',
            ),
        )

    def __str__(self) -> str:
        return f'{self.subscriber} -> {self.author}'
