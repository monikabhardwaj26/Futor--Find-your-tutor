"""
Accounts Forms - Registration, Login, Profile Update
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, TeacherProfile, StudentProfile


class UserRegistrationForm(forms.ModelForm):
    """Form for new user registration."""

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter password (min 8 characters)'
        }),
        min_length=8,
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm your password'
        }),
        label='Confirm Password'
    )

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone_number']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your email address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter phone number (optional)'
            }),
        }

    def clean(self):
        """Validate that both passwords match."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please try again.")
        return cleaned_data

    def save(self, commit=True):
        """Save user with hashed password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Custom login form using email."""

    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email address',
            'autofocus': True
        }),
        label='Email Address'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password'
        }),
        label='Password'
    )


class TeacherProfileForm(forms.ModelForm):
    """Form for teacher profile update."""

    class Meta:
        model = TeacherProfile
        fields = [
            'qualification', 'experience_years', 'subjects',
            'fees_per_month', 'location', 'city', 'teaching_mode',
            'bio', 'demo_video', 'youtube_link', 'is_available'
        ]
        widgets = {
            'qualification': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. M.Sc Mathematics'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'subjects': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Mathematics, Physics, Chemistry'}),
            'fees_per_month': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Monthly fees in INR'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your area/locality'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your city'}),
            'teaching_mode': forms.Select(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Tell students about yourself...'}),
            'youtube_link': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'YouTube demo video link'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class StudentProfileForm(forms.ModelForm):
    """Form for student profile update."""

    class Meta:
        model = StudentProfile
        fields = ['class_name', 'interested_subjects', 'location', 'city']
        widgets = {
            'class_name': forms.Select(attrs={'class': 'form-select'}),
            'interested_subjects': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Mathematics, Science'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your area/locality'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your city'}),
        }


class UserProfileUpdateForm(forms.ModelForm):
    """Form for updating basic user info."""

    class Meta:
        model = CustomUser
        fields = ['full_name', 'phone_number', 'profile_image']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
        }
