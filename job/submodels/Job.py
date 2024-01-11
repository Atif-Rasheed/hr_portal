from django.db import models
from core.models import User
import uuid
from django.core.exceptions import ValidationError
from ..models import JobTemplate

class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='created_%(app_label)s_%(class)s')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='updated_%(app_label)s_%(class)s')
    ip_address = models.GenericIPAddressField(null=True)

    hiring_lead = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    job_template = models.ForeignKey(JobTemplate, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
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
    CANNED_FIELDS_CHOICES = (
        ("0", 'Not Selected, Not Required'),
        ("1", 'Selected, Not Required'),
        ("3", 'Selected, Required'),
    )
    CONFIDENTIAL_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    PRIVATE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    confidential = models.CharField(max_length=255, choices=CONFIDENTIAL_CHOICES,default="No")
    private = models.CharField(max_length=255, choices=PRIVATE_CHOICES,default="No")

    canned_languages = models.BooleanField(default=False, help_text="Language Spoken")
    canned_citizen = models.BooleanField(default=False, help_text="Citizen/Employment Status")
    canned_over18 = models.BooleanField(default=False, help_text="Age 18 or Older")
    canned_felony = models.BooleanField(default=False, help_text="Felony Conviction")
    canned_education = models.BooleanField(default=False, help_text="Highest Education Obtained")
    canned_college = models.BooleanField(default=False, help_text="College/University")
    
    canned_address = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Address")
    canned_cover_letter = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Cover Letter")
    canned_references = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="References")
    canned_wmyu = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="What Makes You Unique")
    canned_linked_in = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="LinkedIn")
    canned_website = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Website, blog or portfolio")
    canned_twitter_username = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Twitter Username")
    canned_start = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Earliest Start Date")
    canned_weekends = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Work Weekends")
    canned_evenings	 = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Work Evenings")
    canned_overtime = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Work Overtime")
    canned_salary = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Desired Salary")
    canned_referral = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Referral Name")
    canned_license = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Valid Drivers License")
    canned_cdl = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Commercial Driving License")
    canned_relocate = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Willing to Relocate")
    canned_gpa = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Grade Point Average(GPA)")
    canned_flighthours = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Pilot - Flight Hours")
    canned_flightgrade = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Pilot - Grade/Ratings")
    canned_felonyexplain = models.CharField(max_length=10, choices=CANNED_FIELDS_CHOICES, default=0,help_text="Felony Explanation")
   
    approved_salary_range_minimum = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Minimum salary",null=True,blank=True)
    approved_salary_range_maximum = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Maximum Salary",null=True,blank=True)
    department = models.CharField(max_length=300,verbose_name="Department", null=True,blank=True)
    country = models.CharField(max_length=255,verbose_name="Country", null=True,blank=True)
    state = models.CharField(max_length=255,verbose_name="State", null=True,blank=True)
    city = models.CharField(max_length=255,verbose_name="City", null=True,blank=True)
    postal_code = models.CharField(max_length=20,verbose_name="Postal Code", null=True,blank=True)
    internal_job_code = models.CharField(max_length=255,verbose_name="Internal Job Code", null=True,blank=True)
    
    JOB_CATEGORY_CHOICES = [
        ('1', 'Executive/Senior Level Officials and Managers'),
        ('2', 'Professionals'),
        ('3', 'Technicians'),
        ('4', 'Sales Workers'),
        ('5', 'Administrative Support Workers'),
        ('6', 'Craft Workers'),
        ('7', 'Operatives'),
        ('8', 'Laborers and Helpers'),
        ('9', 'Service Workers'),
        ('10', 'First/Mid Level Officials & Managers'),
    ]
    

    eeo_1_job_category = models.CharField(max_length=255,verbose_name="Job Category", null=True,blank=True,choices=JOB_CATEGORY_CHOICES)

    SYNDICATION_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    syndication = models.CharField(max_length=255, choices=SYNDICATION_CHOICES,default="No",help_text="Indicates whether the job is syndicated to Indeed, Simply Hired, and other job boards.")
    open_date = models.DateField(null=True,blank=True,verbose_name="Open Date",help_text="The Date that the Job was originally created. Use YYYY-MM-DD format")


    def clean(self):
        if self.approved_salary_range_minimum >= self.approved_salary_range_maximum:
            raise ValidationError("Minimum salary must be less than maximum salary")

    class Meta:
        unique_together = ('hiring_lead','job_id')
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        db_table = "job_jobs"
    
    def __str__(self):
        if self.title:
            return self.title




