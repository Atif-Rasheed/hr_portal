from django.db import models
from core.models import User
import uuid
from django.core.exceptions import ValidationError

class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_jobs')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_jobs',null=True)
    ip_address = models.GenericIPAddressField(null=True)
    title = models.CharField(max_length=100)
    hiring_lead = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    description = models.TextField()
    workflow_id = models.CharField(max_length=150)
    job_id = models.CharField(max_length=150,unique=True,null=True)
    JOB_STATUS_CHOICES = (
        ("1", 'Open (default)'),
        ("3", 'On Hold'),
        ("8", 'Approved'),
        ("7", 'Needs Approval'),
        ("2", 'Drafting'),
        ("4", 'Filled'),
        ("5", 'Canceled'),
        ("6", 'Closed'),
    )
    job_status = models.CharField(max_length=10, choices=JOB_STATUS_CHOICES, default=1)
   
    EMPLOYMENT_TYPE_CHOICES = (
        ("1", 'Full Time'),
        ("2", 'Part Time'),
        ("3", 'Part Time to Full Time'),
        ("4", 'Temporary'),
        ("5", 'Temporary to Full Time'),
        ("6", 'Contracted'),
        ("7", 'Contracted to Full Time'),
        ("8", 'Internship'),
        ("9", 'Internship to Full Time'),
        ("10", 'Volunteer'),
        ("11", 'Seasonal'),
    )
    employment_type = models.CharField(max_length=10, choices=EMPLOYMENT_TYPE_CHOICES, default=1)
    
    MIN_EXP_CHOICES = (
        ("1", 'Student (High School)'),
        ("2", 'Student (College)'),
        ("3", 'Entry Level'),
        ("4", 'Mid Level'),
        ("5", 'Experienced'),
        ("6", 'Manager/Supervisor'),
        ("7", 'Senior Manager/Supervisor'),
        ("8", 'Executive'),
        ("9", 'Senior Executive'),
    )
    minimum_experience = models.CharField(max_length=10, choices=MIN_EXP_CHOICES, default=1)
    CANNED_FELONY_CHOICES = (
        ("0", 'Not Selected, Not Required'),
        ("1", 'Selected, Not Required'),
        ("2", 'Selected, Required'),
    )
    canned_felony = models.CharField(max_length=10, choices=CANNED_FELONY_CHOICES, default=0,verbose_name="Felony Conviction")
    CANNED_EDUCATION_CHOICES = (
        ("0", 'Not Selected, Not Required'),
        ("1", 'Selected, Not Required'),
        ("2", 'Selected, Required'),
    )
    canned_education = models.CharField(max_length=10, choices=CANNED_FELONY_CHOICES, default=0,verbose_name="Highest Education Obtained")
    approved_salary_range_minimum = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Minimum salary",null=True,blank=True)
    approved_salary_range_maximum = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Maximum Salary",null=True,blank=True)


    def clean(self):
        if self.approved_salary_range_minimum >= self.approved_salary_range_maximum:
            raise ValidationError("Minimum salary must be less than maximum salary")

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        db_table = "job_jobs"
    
    def __str__(self):
        if self.title:
            return self.title




