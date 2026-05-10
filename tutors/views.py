"""
Tutors Views - Listing and Detail pages
"""

from django.shortcuts import render, get_object_or_404
from accounts.models import CustomUser, TeacherProfile
from reviews.models import Review


def tutor_list(request):
    """List all available tutors with search/filter."""
    # Get filter parameters from URL
    search_location = request.GET.get('location', '')
    search_subject = request.GET.get('subject', '')
    mode_filter = request.GET.get('mode', '')
    max_fees = request.GET.get('max_fees', '')
    min_experience = request.GET.get('min_exp', '')

    # Start with all available teachers
    teachers = TeacherProfile.objects.filter(is_available=True).select_related('user')

    # Apply filters
    if search_location:
        teachers = teachers.filter(city__icontains=search_location)
    if search_subject:
        teachers = teachers.filter(subjects__icontains=search_subject)
    if mode_filter:
        teachers = teachers.filter(teaching_mode=mode_filter)
    if max_fees:
        teachers = teachers.filter(fees_per_month__lte=max_fees)
    if min_experience:
        teachers = teachers.filter(experience_years__gte=min_experience)

    context = {
        'teachers': teachers,
        'search_location': search_location,
        'search_subject': search_subject,
        'mode_filter': mode_filter,
        'page_title': 'Find Tutors',
    }
    return render(request, 'tutors/tutor_list.html', context)


def tutor_detail(request, pk):
    """Detailed page for a single tutor."""
    teacher_user = get_object_or_404(CustomUser, id=pk, role='teacher')

    try:
        teacher_profile = teacher_user.teacher_profile
    except TeacherProfile.DoesNotExist:
        teacher_profile = None

    # Get all reviews for this teacher
    reviews = Review.objects.filter(teacher=teacher_user).select_related('student')
    avg_rating = teacher_profile.get_average_rating() if teacher_profile else 0

    # Check if current user has already reviewed
    user_review = None
    if request.user.is_authenticated and request.user.role == 'student':
        user_review = reviews.filter(student=request.user).first()

    context = {
        'teacher': teacher_user,
        'profile': teacher_profile,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'user_review': user_review,
        'page_title': f'{teacher_user.full_name} - Tutor Profile',
    }
    return render(request, 'tutors/tutor_detail.html', context)
