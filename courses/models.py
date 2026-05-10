"""
Courses Models
"""

from django.db import models


class Course(models.Model):
    """Model for academic courses/subjects."""

    CLASS_CHOICES = [(str(i), f'Class {i}') for i in range(1, 13)]

    SUBJECT_CHOICES = [
        ('Mathematics', 'Mathematics'),
        ('Science', 'Science'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Computer Science', 'Computer Science'),
        ('Social Science', 'Social Science'),
        ('Sanskrit', 'Sanskrit'),
        ('Economics', 'Economics'),
        ('Accountancy', 'Accountancy'),
    ]

    class_name = models.CharField(max_length=5, choices=CLASS_CHOICES, verbose_name='Class')
    subject_name = models.CharField(max_length=100, choices=SUBJECT_CHOICES, verbose_name='Subject')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        unique_together = ['class_name', 'subject_name']

    def __str__(self):
        return f"Class {self.class_name} - {self.subject_name}"
