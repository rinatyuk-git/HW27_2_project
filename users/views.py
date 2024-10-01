from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer
from users.services import convert_base_to_eur, create_stripe_price, create_stripe_session


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_lesson", "paid_course", "payment_method")
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated]


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_eur = convert_base_to_eur(payment.paid_amount)
        paid_product = []
        if name := payment.paid_course.course_name:
            paid_product.append(name)
        if name := payment.paid_lesson.lesson_name:
            paid_product.append(name)
        paid_product = ', '.join(paid_product)
        price = create_stripe_price(amount_in_eur, paid_product)
        payment_session_id, payment_link = create_stripe_session(price)
        payment.payment_session_id = payment_session_id
        payment.payment_link = payment_link
        payment.save()
