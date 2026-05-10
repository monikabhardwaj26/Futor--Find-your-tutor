"""
Reviews Models
"""

from django.db import models
from accounts.models import CustomUser


class Review(models.Model):
    """Review and rating model for teachers."""

    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='given_reviews',
        limit_choices_to={'role': 'student'}
    )
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='received_reviews',
        limit_choices_to={'role': 'teacher'}
    )
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        unique_together = ['student', 'teacher']   # One review per student per teacher

    def __str__(self):
        return f"{self.student.full_name} → {self.teacher.full_name}: {self.rating}★"
