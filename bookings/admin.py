from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['student', 'teacher', 'subject', 'preferred_date', 'status', 'created_at']
    list_filter = ['status', 'is_demo_class']
    search_fields = ['student__full_name', 'teacher__full_name', 'subject']
    list_editable = ['status']
