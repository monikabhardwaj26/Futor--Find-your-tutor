"""
Reviews Views
"""

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from accounts.models import CustomUser


@login_required
def add_review(request, teacher_id):
    """Add a review for a teacher."""
    if request.user.role != 'student':
        messages.error(request, 'Only students can write reviews.')
        return redirect('home:index')

    teacher = get_object_or_404(CustomUser, id=teacher_id, role='teacher')

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text', '')

        if rating and review_text:
            review, created = Review.objects.update_or_create(
                student=request.user,
                teacher=teacher,
                defaults={'rating': int(rating), 'review_text': review_text}
            )
            if created:
                messages.success(request, 'Review submitted successfully!')
            else:
                messages.success(request, 'Review updated successfully!')
        else:
            messages.error(request, 'Please provide a rating and review.')

    return redirect('tutors:detail', pk=teacher_id)
