from rest_framework import serializers
from .models import ChargingStation, Charger


class ChargerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charger
        fields = ["id", "station", "charger_label", "connector_type", "power_kw", "price_per_kwh", "status"]
        read_only_fields = ["status"]


class ChargingStationListSerializer(serializers.ModelSerializer):
    """Used for the 'Find Charging Stations' list screen — lightweight."""
    status = serializers.CharField(read_only=True)

    class Meta:
        model = ChargingStation
        fields = ["id", "name", "location", "city", "status"]


class ChargingStationDetailSerializer(serializers.ModelSerializer):
    """Used for the 'Station Details' screen — full info + nested chargers."""
    chargers = ChargerSerializer(many=True, read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = ChargingStation
        fields = [
            "id", "name", "location", "city", "operating_hours",
            "latitude", "longitude", "status", "chargers",
        ]
