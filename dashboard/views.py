"""
Dashboard Views - Student and Teacher Dashboards
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import CustomUser, TeacherProfile, StudentProfile
from bookings.models import Booking
from reviews.models import Review


@login_required
def student_dashboard(request):
    """Student dashboard view."""
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Student area only.')
        return redirect('home:index')

    user = request.user

    # Get student profile
    try:
        student_profile = user.student_profile
    except StudentProfile.DoesNotExist:
        student_profile = StudentProfile.objects.create(user=user)

    # Get bookings
    bookings = Booking.objects.filter(student=user).select_related('teacher').order_by('-created_at')
    pending_bookings = bookings.filter(status='pending')
    confirmed_bookings = bookings.filter(status='confirmed')
    completed_bookings = bookings.filter(status='completed')

    # Get favorite tutors
    favorite_tutors = student_profile.favorite_tutors.all()

    context = {
        'page_title': 'Student Dashboard',
        'student_profile': student_profile,
        'all_bookings': bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'completed_bookings': completed_bookings,
        'favorite_tutors': favorite_tutors,
        'total_bookings': bookings.count(),
        'completed_count': completed_bookings.count(),
    }
    return render(request, 'dashboard/student_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    """Teacher dashboard view."""
    if request.user.role != 'teacher':
        messages.error(request, 'Access denied. Teacher area only.')
        return redirect('home:index')

    user = request.user

    # Get teacher profile
    try:
        teacher_profile = user.teacher_profile
    except TeacherProfile.DoesNotExist:
        teacher_profile = TeacherProfile.objects.create(user=user)

    # Get bookings
    bookings = Booking.objects.filter(teacher=user).select_related('student').order_by('-created_at')
    pending_bookings = bookings.filter(status='pending')
    confirmed_bookings = bookings.filter(status='confirmed')
    completed_bookings = bookings.filter(status='completed')

    # Get students (unique students who booked)
    student_ids = bookings.values_list('student_id', flat=True).distinct()
    total_students = CustomUser.objects.filter(id__in=student_ids).count()

    # Get reviews
    reviews = Review.objects.filter(teacher=user).select_related('student')
    avg_rating = teacher_profile.get_average_rating()

    context = {
        'page_title': 'Teacher Dashboard',
        'teacher_profile': teacher_profile,
        'all_bookings': bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'completed_bookings': completed_bookings,
        'total_students': total_students,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'total_reviews': reviews.count(),
        'demo_count': bookings.filter(is_demo_class=True).count(),
    }
    return render(request, 'dashboard/teacher_dashboard.html', context)


@login_required
def toggle_favorite(request, teacher_id):
    """Toggle a teacher as favorite for a student."""
    if request.user.role != 'student':
        return redirect('home:index')

    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('home:index')

    try:
        teacher = CustomUser.objects.get(id=teacher_id, role='teacher')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Tutor not found.')
        return redirect('tutors:list')

    if teacher in student_profile.favorite_tutors.all():
        student_profile.favorite_tutors.remove(teacher)
        messages.info(request, f'{teacher.full_name} removed from favorites.')
    else:
        student_profile.favorite_tutors.add(teacher)
        messages.success(request, f'{teacher.full_name} added to favorites!')

    return redirect('tutors:detail', pk=teacher_id)
