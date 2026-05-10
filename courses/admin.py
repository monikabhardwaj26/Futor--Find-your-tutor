from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'subject_name', 'is_active', 'created_at']
    list_filter = ['class_name', 'is_active']
    search_fields = ['subject_name']
    list_editable = ['is_active']
