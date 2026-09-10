from datetime import datetime, timedelta

from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source="charger.station.name", read_only=True)
    charger_label = serializers.CharField(source="charger.charger_label", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id", "user", "charger", "station_name", "charger_label",
            "booking_date", "start_time", "duration_minutes",
            "estimated_price", "status", "created_at",
        ]
        read_only_fields = ["user", "estimated_price", "status", "created_at"]

    def validate(self, attrs):
        charger = attrs["charger"]
        booking_date = attrs["booking_date"]
        start_time = attrs["start_time"]
        duration = attrs["duration_minutes"]

        start_dt = datetime.combine(booking_date, start_time)
        end_dt = start_dt + timedelta(minutes=duration)

        # Overlap check: same charger, same day, overlapping time range,
        # ignoring cancelled bookings.
        existing = Booking.objects.filter(
            charger=charger,
            booking_date=booking_date,
            status__in=["pending", "confirmed"],
        )
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)

        for b in existing:
            existing_start = datetime.combine(b.booking_date, b.start_time)
            existing_end = existing_start + timedelta(minutes=b.duration_minutes)
            if start_dt < existing_end and existing_start < end_dt:
                raise serializers.ValidationError(
                    "This charger is already booked for an overlapping time slot."
                )

        return attrs

    def create(self, validated_data):
        booking = Booking(**validated_data)
        booking.estimated_price = booking.calculate_estimated_price()
        booking.save()
        return booking
