"""
JOBS MODELS
- Job: Job posting by companies
"""
from django.db import models
from django.contrib.auth.models import User
from accounts.models import Company


class Job(models.Model):
    """
    Job Model: Stores job postings from companies
    - Contains job details, requirements, salary info
    """
    JOB_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('INTERNSHIP', 'Internship'),
        ('CONTRACT', 'Contract'),
    ]

    EXPERIENCE_CHOICES = [
        ('FRESHER', 'Fresher'),
        ('0-1', '0-1 Year'),
        ('1-2', '1-2 Years'),
        ('2-5', '2-5 Years'),
        ('5+', '5+ Years'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField(help_text="Enter skills separated by commas")
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='FULL_TIME')
    experience_required = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='FRESHER')
    location = models.CharField(max_length=200)
    salary_min = models.IntegerField(null=True, blank=True, help_text="Minimum salary in LPA")
    salary_max = models.IntegerField(null=True, blank=True, help_text="Maximum salary in LPA")
    salary_currency = models.CharField(max_length=10, default='INR')
    qualification_required = models.CharField(
        max_length=100,
        choices=[
            ('12TH', '12th Pass'),
            ('DIPLOMA', 'Diploma'),
            ('BACHELORS', 'Bachelors'),
            ('MASTERS', 'Masters'),
        ],
        default='BACHELORS'
    )
    min_cgpa = models.FloatField(default=5.0, help_text="Minimum CGPA required")
    allowed_branches = models.CharField(
        max_length=200,
        help_text="Allowed branches separated by commas (e.g., CSE, ECE, ME)"
    )
    application_deadline = models.DateTimeField()
    max_applications = models.IntegerField(default=100)
    applications_received = models.IntegerField(default=0)
    posted_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return f"{self.title} - {self.company.company_name}"

    def get_required_skills_list(self):
        """Return required skills as a list"""
        return [skill.strip() for skill in self.required_skills.split(',')]

    def get_allowed_branches_list(self):
        """Return allowed branches as a list"""
        return [branch.strip() for branch in self.allowed_branches.split(',')]
