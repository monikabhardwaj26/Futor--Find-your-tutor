from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['student', 'teacher', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['student__full_name', 'teacher__full_name']
