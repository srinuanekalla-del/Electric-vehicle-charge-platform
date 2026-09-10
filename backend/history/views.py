from rest_framework import permissions, viewsets

from .models import ChargingHistory
from .serializers import ChargingHistorySerializer


class ChargingHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/history/ -> the logged-in user's charging history list."""
    serializer_class = ChargingHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChargingHistory.objects.filter(user=self.request.user)
