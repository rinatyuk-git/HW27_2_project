from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def blocking_user():
    """ Проверка пользователей по дате последнего входа и блокировка, если пользователь не заходил более месяца"""
    diff_days = timezone.now() - timedelta(days=30)
    blocked_user = User.objects.filter(last_login__lt=diff_days, is_active=True)
    blocked_user.update(is_active=False)
