from django.contrib import admin
from .models import ChargingHistory

@admin.register(ChargingHistory)
class ChargingHistoryAdmin(admin.ModelAdmin):
    list_display = ["user", "station_name", "date", "energy_consumed_kwh", "amount_paid", "status"]
    list_filter = ["status"]
