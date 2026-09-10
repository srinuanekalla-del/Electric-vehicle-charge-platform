from rest_framework import serializers
from .models import ChargingHistory


class ChargingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingHistory
        fields = ["id", "station_name", "date", "energy_consumed_kwh", "amount_paid", "status"]
