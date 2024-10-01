from rest_framework import serializers

from users.models import User, Payments
from users.services import convert_base_to_eur


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class PaymentsSerializer(serializers.ModelSerializer):
    eur_price = serializers.SerializerMethodField()

    def get_eur_price(self, instance):
        return convert_base_to_eur(instance.paid_amount)

    class Meta:
        model = Payments
        fields = "__all__"
