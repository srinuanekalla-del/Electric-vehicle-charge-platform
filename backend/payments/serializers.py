from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "booking", "transaction_id", "amount", "method", "status", "paid_at"]
        read_only_fields = ["transaction_id", "amount", "status", "paid_at"]
