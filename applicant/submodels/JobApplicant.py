from django.db import models
from core.models import User
from job.models import Job
import uuid

class JobApplicant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="c_%(app_label)s_%(class)ss",null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="u_%(app_label)s_%(class)ss",null=True)
    ip_address = models.GenericIPAddressField(null=True)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recruiter_%(app_label)s_%(class)ss", null=True)
    applicant_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254,verbose_name="Email",null=True)
    address = models.TextField(verbose_name = "Address",null=True,blank=True)
    location = models.TextField(verbose_name = "Location",null=True,blank=True)
    prospect_phone = models.CharField(max_length=255)
    linkedin_url = models.URLField(verbose_name="LinkedIn Url",blank=True, null=True)
    eeo_gender = models.CharField(max_length=255, blank=True, null=True,verbose_name = "EEO Gender")
    eeo_race = models.CharField(max_length=255, blank=True, null=True,verbose_name = "EEO Race")
    eeo_disability = models.CharField(max_length=255, blank=True, null=True,verbose_name = "EEO Disability")
    website = models.URLField(blank=True, null=True,verbose_name="Website")
    desired_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,verbose_name ="Desired Salary")
    desired_start_date = models.DateField(blank=True, null=True)
    referrer = models.CharField(max_length=255, blank=True, null=True,verbose_name="Referrer")
    languages = models.TextField(blank=True, null=True,verbose_name="Languages")
    wmyu = models.CharField(max_length=255, blank=True, null=True)
    has_driver_license = models.CharField(max_length=255, choices=[("Yes", "Yes"), ("No", "No"), ("No answer", "No answer")], default="No answer")
    willing_to_relocate = models.CharField(max_length=255, choices=[("Yes", "Yes"), ("No", "No"), ("No answer", "No answer")], default="No answer")
    citizenship_status = models.CharField(max_length=255, choices=[("Yes", "Yes"), ("No", "No"), ("No answer", "No answer")], default="No answer")
    education_level = models.CharField(max_length=255, choices=[("High School", "High School"), ("Bachelor's", "Bachelor's"), ("Master's", "Master's"), ("Ph.D.", "Ph.D."), ("No answer", "No answer")], default="No answer")
    has_cdl = models.CharField(max_length=255, choices=[("Yes", "Yes"), ("No", "No"), ("No answer", "No answer")], default="No answer")
    over_18 = models.CharField(max_length=255, choices=[("Yes", "Yes"), ("No", "No"), ("No answer", "No answer")], default="No answer")
    can_work_weekends = models.CharField(max_length=255, choices=[("Yes", "Yes"), ("No", "No"), ("No answer", "No answer")], default="No answer")
    can_work_evenings = models.CharField(max_length=255, choices=[("Yes", "Yes"), ("No", "No"), ("No answer", "No answer")], default="No answer")
    can_work_overtime = models.CharField(max_length=255, choices=[("Yes", "Yes"), ("No", "No"), ("No answer", "No answer")], default="No answer")
    has_felony = models.CharField(max_length=255, choices=[("Yes", "Yes"), ("No", "No"), ("No answer", "No answer")], default="No answer")
    felony_explanation = models.TextField(blank=True, null=True)
    twitter_username = models.CharField(max_length=255, blank=True, null=True)
    college_gpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    apply_date = models.DateField()
    comments_count = models.IntegerField(default=0)
    source = models.CharField(max_length=255, choices=[("LINKEDIN", "LinkedIn"), ("OTHER", "Other")], default="LINKEDIN")
    eeoc_veteran = models.BooleanField(default=False)
    eeoc_disability = models.BooleanField(default=False)
    eeoc_disability_signature = models.CharField(max_length=255, blank=True, null=True)
    eeoc_disability_date = models.DateField(blank=True, null=True)
    resume_link = models.URLField(blank=True, null=True)

    @property
    def progress(self):
        # if self.total_tasks == 0:
        #     return 0
        # return (self.completed_tasks / self.total_tasks) * 100
        return 50

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        self.progress_bar = self.progress
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = 'Applicant'
        verbose_name_plural = 'Applicants'
        db_table = "applicant_applicants"


