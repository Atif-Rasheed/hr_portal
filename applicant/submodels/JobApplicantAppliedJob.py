from django.db import models
from core.models import User
from job.models import Job
from applicant.models import JobApplicant
import uuid

class JobApplicantAppliedJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="c_%(app_label)s_%(class)ss",null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="u_%(app_label)s_%(class)ss",null=True)
    ip_address = models.GenericIPAddressField(null=True)
    applicant = models.ForeignKey(JobApplicant, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)ss", null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)ss", null=True)
    hiring_lead_rating = models.CharField(max_length=255)
    average_rating = models.CharField(max_length=255)
    applicant_progress =  models.CharField(max_length=255)
    workflow_step_id =  models.CharField(max_length=255,null=True)
    job_title =  models.CharField(max_length=255)

    def __str__(self):
        return f"{self.applicant.full_name} applied for {self.job_title}"

    class Meta:
        verbose_name = 'Applicant Applied Job'
        verbose_name_plural = 'Applicant Applied Jobs'
        db_table = "applicant_applicant_applied_jobs"


