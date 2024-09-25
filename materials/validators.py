import re

from rest_framework.serializers import ValidationError


correct_url = 'https://www.youtube.com'


def validate_lesson_url(value):
    if not value.startswith(correct_url):
        raise ValidationError("ссылки на видео можно прикреплять только с https://www.youtube.com/")


# class UrlLessonValidator:
#     correct_url = 'https://www.youtube.com/'
#
#     def __init__(self, field):
#         self.field = field
#
#     def __call__(self, value):
#         """ проверка на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com """
#         reg = re.compile(r'https://www.youtube.com/')
#         tmp_val = dict(value).get(self.field)
#         if not bool(reg.match(tmp_val)):
#         # if bool(reg.search(tmp_val)):
#             raise ValidationError("ссылки на видео можно прикреплять только с https://www.youtube.com/")
