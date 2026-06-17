"""
ACCOUNTS MODELS
- Student: User profile for students with resume and skills
- Company: User profile for companies with details
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Student(models.Model):
    """
    Student Model: Extends Django User with placement portal specific fields
    - Stores student info, skills, resume
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    roll_no = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    cgpa = models.FloatField(default=0.0)
    skills = models.TextField(help_text="Enter skills separated by commas (e.g., Python, Java, Django)")
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        null=True,
        blank=True
    )
    branch = models.CharField(
        max_length=50,
        choices=[
            ('CSE', 'Computer Science'),
            ('ECE', 'Electronics'),
            ('ME', 'Mechanical'),
            ('CE', 'Civil'),
            ('EE', 'Electrical'),
        ]
    )
    year = models.IntegerField(choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')])
    applied_jobs = models.IntegerField(default=0)
    placed = models.BooleanField(default=False)
    placement_offer = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.first_name} ({self.roll_no})"

    def get_skills_list(self):
        """Return skills as a list"""
        return [skill.strip() for skill in self.skills.split(',')]


class Company(models.Model):
    """
    Company Model: Extends Django User with company specific fields
    - Stores company info, headquarters, hiring details
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    logo = models.FileField(upload_to='company_logos/', null=True, blank=True)
    jobs_posted = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.company_name
