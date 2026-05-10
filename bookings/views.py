"""
Bookings Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from accounts.models import CustomUser


@login_required
def book_demo(request, teacher_id):
    """Book a demo class with a teacher."""
    teacher = get_object_or_404(CustomUser, id=teacher_id, role='teacher')

    if request.method == 'POST':
        subject = request.POST.get('subject')
        preferred_date = request.POST.get('preferred_date')
        preferred_time = request.POST.get('preferred_time')
        message = request.POST.get('message', '')

        if subject and preferred_date and preferred_time:
            Booking.objects.create(
                student=request.user,
                teacher=teacher,
                subject=subject,
                preferred_date=preferred_date,
                preferred_time=preferred_time,
                message=message,
            )
            messages.success(request, f'Demo class booked with {teacher.full_name}! They will contact you soon.')
            return redirect('dashboard:student')
        else:
            messages.error(request, 'Please fill all required fields.')

    context = {
        'teacher': teacher,
        'page_title': f'Book Demo - {teacher.full_name}'
    }
    return render(request, 'bookings/book_demo.html', context)


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking."""
    booking = get_object_or_404(Booking, id=booking_id, student=request.user)
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    return redirect('dashboard:student')


@login_required
def update_booking_status(request, booking_id):
    """Teacher updates booking status."""
    booking = get_object_or_404(Booking, id=booking_id, teacher=request.user)
    new_status = request.POST.get('status')
    if new_status in ['confirmed', 'completed', 'cancelled']:
        booking.status = new_status
        booking.save()
        messages.success(request, f'Booking status updated to {new_status}.')
    return redirect('dashboard:teacher')
