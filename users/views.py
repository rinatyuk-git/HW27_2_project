from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    fields = ("email", "phone", "city", "avatar", )


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_lesson", "paid_course", "payment_method")
    ordering_fields = ('payment_date',)
