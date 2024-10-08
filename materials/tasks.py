from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Subscription


@shared_task
def course_updated_message(id):
    """ Подготовка рассылки писем пользователям об обновлении курса """
    updated_course = Subscription.objects.filter(course_name=id)
    for item in updated_course:
        send_mail(
            'Course updated',
            'Course updated info',
            EMAIL_HOST_USER,
            [item.user.email]
        )
