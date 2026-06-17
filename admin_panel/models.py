"""
ADMIN PANEL MODELS
- AdminStats: Store statistics and analytics data
"""
from django.db import models


class AdminStats(models.Model):
    """
    AdminStats Model: Stores portal statistics for dashboard
    """
    total_students = models.IntegerField(default=0)
    total_companies = models.IntegerField(default=0)
    total_jobs = models.IntegerField(default=0)
    total_applications = models.IntegerField(default=0)
    students_placed = models.IntegerField(default=0)
    pending_verifications = models.IntegerField(default=0)
    average_salary = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Admin Stats"

    def __str__(self):
        return f"Stats - Updated: {self.last_updated}"
