from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "charger", "booking_date", "start_time", "duration_minutes", "estimated_price", "status"]
    list_filter = ["status"]
