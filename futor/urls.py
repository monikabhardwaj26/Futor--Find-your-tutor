"""
Futor - Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # App URLs
    path('', include('home.urls')),                     # Home page
    path('accounts/', include('accounts.urls')),        # Login, Register, Role select
    path('courses/', include('courses.urls')),          # Courses page
    path('tutors/', include('tutors.urls')),            # Tutors listing/detail
    path('dashboard/', include('dashboard.urls')),      # Student & Teacher dashboards
    path('bookings/', include('bookings.urls')),        # Booking system
    path('reviews/', include('reviews.urls')),          # Reviews
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
