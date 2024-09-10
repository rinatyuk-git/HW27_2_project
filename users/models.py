from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name="Почтовый адрес",
        unique=True,
    )  # авторизацию заменить на email
    phone = models.CharField(
        max_length=35,
        verbose_name="Номер телефона",
        blank=True,
        null=True,
    )  # номер телефона,
    city = models.CharField(
        max_length=55,
        verbose_name="Город",
        blank=True,
        null=True,
    )  # город,
    avatar = models.ImageField(
        upload_to="users/images",
        verbose_name="Аватар пользователя",
        help_text="Загрузите аватар пользователя",
        blank=True,
        null=True,
    )  # аватар,
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
