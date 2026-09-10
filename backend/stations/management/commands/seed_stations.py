from django.core.management.base import BaseCommand
from stations.models import ChargingStation, Charger


class Command(BaseCommand):
    help = "Seed sample charging stations and chargers into the database."

    def handle(self, *args, **options):
        if ChargingStation.objects.exists():
            self.stdout.write(self.style.WARNING("Stations already exist. Skipping."))
            return

        data = [
            {
                "station": {"name": "GreenCharge Station", "location": "MG Road", "city": "Bengaluru",
                            "operating_hours": "6:00 AM - 11:00 PM", "latitude": 12.9758, "longitude": 77.6045},
                "chargers": [
                    {"charger_label": "Charger 1", "connector_type": "Type2", "power_kw": 22, "price_per_kwh": 18},
                    {"charger_label": "Charger 2", "connector_type": "CCS", "power_kw": 50, "price_per_kwh": 18, "status": "busy"},
                ],
            },
            {
                "station": {"name": "EV Point Mall", "location": "Forum Mall, Koramangala", "city": "Bengaluru",
                            "operating_hours": "10:00 AM - 10:00 PM", "latitude": 12.9352, "longitude": 77.6146},
                "chargers": [
                    {"charger_label": "Charger 1", "connector_type": "Type2", "power_kw": 11, "price_per_kwh": 20},
                    {"charger_label": "Charger 2", "connector_type": "CCS", "power_kw": 150, "price_per_kwh": 20},
                ],
            },
            {
                "station": {"name": "ChargeHub Tech Park", "location": "Outer Ring Road", "city": "Bengaluru",
                            "operating_hours": "24/7", "latitude": 12.9569, "longitude": 77.6961},
                "chargers": [
                    {"charger_label": "Charger 1", "connector_type": "Type2", "power_kw": 22, "price_per_kwh": 17},
                ],
            },
        ]

        for entry in data:
            station = ChargingStation.objects.create(**entry["station"])
            for c in entry["chargers"]:
                Charger.objects.create(station=station, **c)

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(data)} stations with chargers."))
