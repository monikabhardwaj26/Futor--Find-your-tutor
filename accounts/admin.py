"""
Accounts Admin Configuration
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TeacherProfile, StudentProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin Panel."""

    list_display = ['full_name', 'email', 'role', 'phone_number', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['full_name', 'email', 'phone_number']
    ordering = ['-date_joined']

    fieldsets = (
        ('Basic Info', {'fields': ('email', 'full_name', 'phone_number', 'profile_image')}),
        ('Role & Access', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Password', {'fields': ('password',)}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
    )

    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    """Teacher Profile Admin."""

    list_display = ['user', 'qualification', 'experience_years', 'fees_per_month', 'city', 'is_verified', 'is_available']
    list_filter = ['is_verified', 'is_available', 'teaching_mode']
    search_fields = ['user__full_name', 'user__email', 'subjects', 'city']
    list_editable = ['is_verified', 'is_available']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Student Profile Admin."""

    list_display = ['user', 'class_name', 'city', 'created_at']
    list_filter = ['class_name']
    search_fields = ['user__full_name', 'user__email', 'city']
