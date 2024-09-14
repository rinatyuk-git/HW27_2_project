from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import Payments, User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        payment_list = [
            {'user': User(1), 'payment_date': '2024-10-26', 'paid_course': Course(5), 'paid_lesson': Lesson(8), 'paid_amount': 59000, 'payment_method': 'BANK'},
            {'user': User(2), 'payment_date': '2024-10-02', 'paid_course': Course(2), 'paid_lesson': Lesson(5), 'paid_amount': 39000, 'payment_method': 'BANK'},
            {'user': User(3), 'payment_date': '2024-08-26', 'paid_course': Course(3), 'paid_lesson': Lesson(3), 'paid_amount': 64000, 'payment_method': 'BANK'},
        ]
        payments_for_create = []
        for item in payment_list:
            payments_for_create.append(
                Payments(**item)
            )

        Payments.objects.bulk_create(payments_for_create)