"""
Accounts Views - Registration, Login, Logout, Role Selection
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, TeacherProfileForm, StudentProfileForm, UserProfileUpdateForm
from .models import CustomUser, TeacherProfile, StudentProfile


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('home:index')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Futor, {user.full_name}! Please select your role.')
            return redirect('accounts:role_select')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form, 'page_title': 'Register'})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('home:index')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.full_name}!')

            # If role not set, go to role selection
            if not user.role:
                return redirect('accounts:role_select')

            # Otherwise go to respective dashboard
            if user.role == 'teacher':
                return redirect('dashboard:teacher')
            else:
                return redirect('dashboard:student')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'page_title': 'Login'})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home:index')


@login_required
def role_select_view(request):
    """Allow user to select role: student or teacher."""
    if request.user.role:
        # Already has a role, redirect to dashboard
        if request.user.role == 'teacher':
            return redirect('dashboard:teacher')
        return redirect('dashboard:student')

    if request.method == 'POST':
        role = request.POST.get('role')
        if role in ['student', 'teacher']:
            request.user.role = role
            request.user.save()

            # Create profile based on role
            if role == 'teacher':
                TeacherProfile.objects.get_or_create(user=request.user)
                messages.success(request, 'Welcome Teacher! Please complete your profile.')
                return redirect('dashboard:teacher')
            else:
                StudentProfile.objects.get_or_create(user=request.user)
                messages.success(request, 'Welcome Student! Start exploring tutors.')
                return redirect('dashboard:student')
        else:
            messages.error(request, 'Please select a valid role.')

    return render(request, 'accounts/role_select.html', {'page_title': 'Select Role'})


@login_required
def profile_view(request):
    """View and update user profile."""
    user = request.user

    if request.method == 'POST':
        user_form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)

        if user.role == 'teacher':
            profile_form = TeacherProfileForm(request.POST, request.FILES, instance=user.teacher_profile)
        else:
            profile_form = StudentProfileForm(request.POST, instance=user.student_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserProfileUpdateForm(instance=user)

        if user.role == 'teacher':
            try:
                profile = user.teacher_profile
            except TeacherProfile.DoesNotExist:
                profile = TeacherProfile.objects.create(user=user)
            profile_form = TeacherProfileForm(instance=profile)
        else:
            try:
                profile = user.student_profile
            except StudentProfile.DoesNotExist:
                profile = StudentProfile.objects.create(user=user)
            profile_form = StudentProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'page_title': 'My Profile'
    }
    return render(request, 'accounts/profile.html', context)
