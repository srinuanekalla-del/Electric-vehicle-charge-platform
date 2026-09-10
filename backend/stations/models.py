from django.db import models


class ChargingStation(models.Model):
    """
    A physical EV charging location. Stored permanently in the database —
    this is the data that powers the 'Find Charging Stations' and
    'Station Details' screens.
    """

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)          # e.g. "MG Road, Bengaluru"
    city = models.CharField(max_length=100)
    operating_hours = models.CharField(max_length=100, default="24/7")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.city})"

    @property
    def status(self):
        """
        'Available / Busy' status shown in the station list —
        Available if at least one charger at this station is free.
        """
        if self.chargers.filter(status="available").exists():
            return "Available"
        return "Busy"


class Charger(models.Model):
    """A single charging point belonging to a ChargingStation."""

    CONNECTOR_CHOICES = (
        ("Type1", "Type 1"),
        ("Type2", "Type 2"),
        ("CCS", "CCS"),
        ("CHAdeMO", "CHAdeMO"),
    )
    STATUS_CHOICES = (
        ("available", "Available"),
        ("busy", "Busy"),
    )

    station = models.ForeignKey(ChargingStation, related_name="chargers", on_delete=models.CASCADE)
    charger_label = models.CharField(max_length=50)        # e.g. "Charger 1"
    connector_type = models.CharField(max_length=20, choices=CONNECTOR_CHOICES)
    power_kw = models.DecimalField(max_digits=6, decimal_places=2)
    price_per_kwh = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="available")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.charger_label} - {self.station.name} ({self.get_status_display()})"
