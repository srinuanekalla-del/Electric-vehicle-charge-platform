from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    POST /api/bookings/            -> 'Book Charging Slot' (conflict-checked, price calculated)
    GET  /api/bookings/             -> user's own bookings
    POST /api/bookings/{id}/cancel/ -> cancel a booking
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status="pending")  # awaits payment

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status in ["completed", "cancelled"]:
            return Response({"detail": f"Cannot cancel a {booking.status} booking."}, status=400)
        booking.status = "cancelled"
        booking.save(update_fields=["status"])
        return Response(BookingSerializer(booking).data)
