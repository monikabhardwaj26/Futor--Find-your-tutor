"""
Courses Views
"""

from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import TeacherProfile, CustomUser


def courses_view(request):
    """Main courses page - class and subject selection."""

    # Get filter parameters
    selected_class = request.GET.get('class_name', '')
    selected_subject = request.GET.get('subject', '')
    location_filter = request.GET.get('location', '')
    mode_filter = request.GET.get('mode', '')

    # All class options
    classes = [str(i) for i in range(1, 13)]

    # Subjects by class level
    primary_subjects = ['Mathematics', 'English', 'Hindi', 'Science', 'Social Science']
    secondary_subjects = primary_subjects + ['Computer Science', 'Sanskrit']
    senior_subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'Computer Science', 'Economics', 'Accountancy']

    # Determine subjects based on class
    subjects = []
    if selected_class:
        class_num = int(selected_class)
        if class_num <= 5:
            subjects = primary_subjects
        elif class_num <= 10:
            subjects = secondary_subjects
        else:
            subjects = senior_subjects

    # Filter tutors
    tutors = []
    if selected_class and selected_subject:
        teacher_profiles = TeacherProfile.objects.filter(
            is_available=True,
            subjects__icontains=selected_subject
        ).select_related('user')

        if location_filter:
            teacher_profiles = teacher_profiles.filter(
                city__icontains=location_filter
            )
        if mode_filter:
            teacher_profiles = teacher_profiles.filter(teaching_mode=mode_filter)

        tutors = teacher_profiles

    context = {
        'page_title': 'Courses',
        'classes': classes,
        'subjects': subjects,
        'selected_class': selected_class,
        'selected_subject': selected_subject,
        'location_filter': location_filter,
        'mode_filter': mode_filter,
        'tutors': tutors,
    }
    return render(request, 'courses/courses.html', context)


def get_subjects_ajax(request):
    """AJAX endpoint: return subjects for a given class."""
    class_name = request.GET.get('class_name', '')
    subjects = []

    if class_name:
        class_num = int(class_name)
        if class_num <= 5:
            subjects = ['Mathematics', 'English', 'Hindi', 'Science', 'Social Science']
        elif class_num <= 10:
            subjects = ['Mathematics', 'English', 'Hindi', 'Science', 'Social Science', 'Computer Science', 'Sanskrit']
        else:
            subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'Computer Science', 'Economics', 'Accountancy', 'Hindi']

    return JsonResponse({'subjects': subjects})
