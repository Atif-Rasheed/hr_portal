from django.db import models
from job.models import Job
from core.models import User
import uuid

class KnockoutCriteria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_criteria_knockout')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_criteria_knockout',null=True)
    ip_address = models.GenericIPAddressField(null=True)
    JOB_TITLES = [
        ('job1', 'Job Title 1'),
        ('job2', 'Job Title 2'),
        # Add other job titles as needed
    ]

    MINIMUM_EXPERIENCE_CHOICES = [
        ('experience1', 'Experience 1'),
        ('experience2', 'Experience 2'),
        # Add other experience options as needed
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_criteria_knockout')
    minimum_experience = models.CharField(max_length=50, choices=MINIMUM_EXPERIENCE_CHOICES)
    job_description_option = models.CharField(max_length=50, choices=[('template', 'Template'), ('manual', 'Manual')])
    manual_job_description = models.TextField(blank=True)
    education_level = models.CharField(max_length=50, blank=True)
    multiple_languages = models.BooleanField(default=False)
    no_college = models.BooleanField(default=False)
    felon = models.BooleanField(default=False)
    no_references = models.BooleanField(default=False)
    not_citizen = models.BooleanField(default=False)

    def __str__(self):
        return f"Knockout Criteria for {self.job_title}"