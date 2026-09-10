from django.conf import settings
from django.db import models


class ChargingHistory(models.Model):
    """
    Powers the 'Charging History' screen: previous (and upcoming) sessions,
    with energy consumed and amount paid. Created automatically when a
    payment succeeds (see payments/views.py), and updated when a session
    actually finishes.
    """

    STATUS_CHOICES = (
        ("upcoming", "Upcoming"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="charging_history", on_delete=models.CASCADE)
    booking = models.OneToOneField("bookings.Booking", related_name="history_entry", on_delete=models.CASCADE)

    station_name = models.CharField(max_length=200)
    date = models.DateField()
    energy_consumed_kwh = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="upcoming")

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Charging histories"

    def __str__(self):
        return f"{self.user.username} - {self.station_name} - {self.date}"
