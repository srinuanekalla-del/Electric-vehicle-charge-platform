from django.contrib import admin
from .models import ChargingStation, Charger

class ChargerInline(admin.TabularInline):
    model = Charger
    extra = 1

@admin.register(ChargingStation)
class ChargingStationAdmin(admin.ModelAdmin):
    list_display = ["name", "city", "operating_hours", "is_active"]
    list_filter = ["city", "is_active"]
    search_fields = ["name", "city"]
    inlines = [ChargerInline]

@admin.register(Charger)
class ChargerAdmin(admin.ModelAdmin):
    list_display = ["charger_label", "station", "connector_type", "power_kw", "price_per_kwh", "status"]
    list_filter = ["connector_type", "status"]
