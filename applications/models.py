"""
APPLICATIONS MODELS
- Application: Job application by students
"""
from django.db import models
from accounts.models import Student
from jobs.models import Job


class Application(models.Model):
    """
    Application Model: Stores job applications by students
    - Tracks application status and timestamps
    """
    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('SHORTLISTED', 'Shortlisted'),
        ('REJECTED', 'Rejected'),
        ('INTERVIEW', 'Interview Round'),
        ('SELECTED', 'Selected'),
        ('OFFER_RECEIVED', 'Offer Received'),
        ('OFFER_ACCEPTED', 'Offer Accepted'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    cover_letter = models.TextField(blank=True)
    resume_used = models.FileField(upload_to='resumes/', null=True, blank=True)
    skill_match_percentage = models.IntegerField(default=0, help_text="0-100")
    notes = models.TextField(blank=True, help_text="Notes from company/admin")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'job')
        ordering = ['-applied_on']

    def __str__(self):
        return f"{self.student.user.first_name} - {self.job.title} - {self.status}"

    def calculate_skill_match(self):
        """
        Calculate skill match percentage between student and job
        Returns: percentage of matching skills
        """
        student_skills = set(self.student.get_skills_list())
        job_skills = set(self.job.get_required_skills_list())
        
        if not job_skills:
            return 0
        
        matching_skills = student_skills.intersection(job_skills)
        match_percentage = (len(matching_skills) / len(job_skills)) * 100
        self.skill_match_percentage = int(match_percentage)
        self.save()
        return self.skill_match_percentage
