from bookings.models import Booking
from history.models import ChargingHistory
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment
from .serializers import PaymentSerializer


class MakePaymentView(APIView):
    """
    POST /api/payments/
    Body: { "booking_id": <id>, "method": "card" }

    Confirms payment for a pending booking:
      - creates a Payment record with the booking's estimated_price
      - moves the booking to 'confirmed'
      - creates a ChargingHistory row (status: upcoming) for the 'Charging History' screen
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        booking_id = request.data.get("booking_id")
        method = request.data.get("method", "card")

        booking = Booking.objects.filter(id=booking_id, user=request.user).first()
        if not booking:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)
        if booking.status != "pending":
            return Response(
                {"detail": f"Booking is '{booking.status}', cannot pay for it."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if hasattr(booking, "payment"):
            return Response({"detail": "This booking has already been paid for."}, status=400)

        payment = Payment.objects.create(
            booking=booking,
            amount=booking.estimated_price,
            method=method,
            status="success",
        )

        booking.status = "confirmed"
        booking.save(update_fields=["status"])

        ChargingHistory.objects.create(
            user=request.user,
            booking=booking,
            station_name=booking.charger.station.name,
            date=booking.booking_date,
            energy_consumed_kwh=0,     # filled in once the session actually completes
            amount_paid=payment.amount,
            status="upcoming",
        )

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
