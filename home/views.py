"""
Home Views - Main landing page
"""

from django.shortcuts import render
from accounts.models import TeacherProfile


def index(request):
    """Main home page with featured tutors."""
    # Get 6 featured/verified tutors for the homepage
    featured_tutors = TeacherProfile.objects.filter(
        is_available=True
    ).select_related('user').order_by('-is_verified')[:6]

    context = {
        'featured_tutors': featured_tutors,
        'page_title': 'Futor - Find Trusted Tutors in Your Area',
    }
    return render(request, 'home/index.html', context)


def about_view(request):
    """About Futor page."""
    return render(request, 'home/about.html', {'page_title': 'About Futor'})


def contact_view(request):
    """Contact page."""
    from django.contrib import messages
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        # In a real project, send email here
        messages.success(request, f'Thank you {name}! We will get back to you soon.')
    return render(request, 'home/contact.html', {'page_title': 'Contact Us'})
