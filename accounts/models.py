"""
Accounts Models - Custom User, Teacher Profile, Student Profile
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser model using email instead of username."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model with email-based authentication.
    Roles: student or teacher
    """

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]

    # Basic fields
    full_name = models.CharField(max_length=150, verbose_name='Full Name')
    email = models.EmailField(unique=True, verbose_name='Email Address')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        default=None
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
        verbose_name='User Role'
    )

    # Django required fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Use email for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def get_full_name(self):
        return self.full_name

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'


class TeacherProfile(models.Model):
    """Extended profile for teachers."""

    TEACHING_MODE_CHOICES = [
        ('online', 'Online Only'),
        ('offline', 'Offline / Home Tuition'),
        ('both', 'Both Online & Offline'),
    ]

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    qualification = models.CharField(max_length=200, blank=True)
    experience_years = models.PositiveIntegerField(default=0, verbose_name='Experience (Years)')
    subjects = models.CharField(max_length=500, blank=True, help_text='Comma separated subjects')
    fees_per_month = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    location = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    teaching_mode = models.CharField(
        max_length=10,
        choices=TEACHING_MODE_CHOICES,
        default='both'
    )
    bio = models.TextField(blank=True)
    demo_video = models.FileField(upload_to='demo_videos/', blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Teacher Profile'
        verbose_name_plural = 'Teacher Profiles'

    def __str__(self):
        return f"Teacher: {self.user.full_name}"

    def get_subjects_list(self):
        """Return subjects as a list."""
        return [s.strip() for s in self.subjects.split(',') if s.strip()]

    def get_average_rating(self):
        """Calculate average rating from reviews."""
        reviews = self.user.received_reviews.all()
        if reviews.exists():
            total = sum([r.rating for r in reviews])
            return round(total / reviews.count(), 1)
        return 0


class StudentProfile(models.Model):
    """Extended profile for students."""

    CLASS_CHOICES = [(str(i), f'Class {i}') for i in range(1, 13)]

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    class_name = models.CharField(
        max_length=5,
        choices=CLASS_CHOICES,
        blank=True,
        verbose_name='Current Class'
    )
    interested_subjects = models.CharField(
        max_length=500,
        blank=True,
        help_text='Comma separated subjects'
    )
    location = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    favorite_tutors = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name='favorited_by',
        limit_choices_to={'role': 'teacher'}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'

    def __str__(self):
        return f"Student: {self.user.full_name}"

    def get_subjects_list(self):
        return [s.strip() for s in self.interested_subjects.split(',') if s.strip()]
