from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


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


class Payments(models.Model):
    PAYMENT_CHOICES = [
        ("CASH", "наличные"),
        ("BANK", "перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )  # пользователь
    payment_date = models.DateField(
        verbose_name='Дата оплаты',
        help_text="Укажите дату оплаты"
    )  # дата оплаты
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )  # оплаченный курс
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )  # оплаченный урок
    paid_amount = models.PositiveIntegerField(
        verbose_name='Сумма оплаты',
        help_text="Укажите сумму оплаты"
    )  # сумма оплаты
    payment_method = models.CharField(
        max_length=50,
        verbose_name='Способ оплаты',
        help_text='Выбрать способ оплаты',
        choices=PAYMENT_CHOICES,
        default="BANK",
    )  # способ оплаты