from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from .models import ChargingStation, Charger
from .serializers import ChargerSerializer, ChargingStationDetailSerializer, ChargingStationListSerializer


class ChargingStationViewSet(viewsets.ModelViewSet):
    """
    GET  /api/stations/          -> 'Find Charging Stations' list (search by ?search=city or name)
    GET  /api/stations/{id}/     -> 'Station Details' screen
    POST/PUT/DELETE              -> manage stations (auth required)
    """
    queryset = ChargingStation.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["city"]
    search_fields = ["name", "city", "location"]

    def get_serializer_class(self):
        return ChargingStationDetailSerializer if self.action == "retrieve" else ChargingStationListSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class ChargerViewSet(viewsets.ModelViewSet):
    """Used by the 'Select Charger' screen — GET /api/chargers/?station=<id>"""
    queryset = Charger.objects.all()
    serializer_class = ChargerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["station", "status"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
