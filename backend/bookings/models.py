from django.conf import settings
from django.db import models


class Booking(models.Model):
    """
    Represents 'Select Date & Time' + 'Book Charging Slot' in the flow.
    Estimated price is calculated at booking time from charger rate x duration.
    """

    STATUS_CHOICES = (
        ("pending", "Pending Payment"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="bookings", on_delete=models.CASCADE)
    charger = models.ForeignKey("stations.Charger", related_name="bookings", on_delete=models.CASCADE)

    booking_date = models.DateField()
    start_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField()   # "Select charging duration"

    estimated_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} - {self.charger}"

    def calculate_estimated_price(self):
        """price = charger's price_per_kwh x power_kw x hours (simple estimate)."""
        hours = self.duration_minutes / 60
        return round(float(self.charger.price_per_kwh) * float(self.charger.power_kw) * hours, 2)
