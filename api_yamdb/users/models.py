from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models


class User(AbstractUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_superuser:
            self.role = "admin"

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="недопустимый username",
            )
        ],
        verbose_name="Юзернейм",
    )
    email = models.EmailField(
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True,
        blank=False,
        validators=(MaxLengthValidator(settings.EMAIL_MAX_LENGTH),),
        verbose_name="Email"
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Фамилия"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="О себе"
    )
    role = models.CharField(
        max_length=20,
        choices=USER_ROLE_CHOICES,
        default=USER,
        verbose_name="Роль",
    )
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Код подтверждения"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_username_email"
            )
        ]
        ordering = ["username"]

    @property
    def is_moderator(self):
        """Возращает True, если пользователь является модератором"""
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        """Возращает True, если пользователь является админом"""
        return self.role == self.ADMIN
