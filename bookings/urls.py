from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<int:teacher_id>/', views.book_demo, name='book_demo'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('update/<int:booking_id>/', views.update_booking_status, name='update_status'),
]
