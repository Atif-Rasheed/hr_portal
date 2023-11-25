from django.db import models
from core.models import User
from job.models import Job
import uuid

class JobApplicant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_user',null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_user',null=True)
    ip_address = models.GenericIPAddressField(null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_jobs')
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recruiter_user', null=True)

    applicant_id = models.CharField(max_length=255)
    city = models.CharField(max_length=255,null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    prospect_phone = models.CharField(max_length=255)
    apply_date = models.DateField()
    status = models.CharField(max_length=255,null=True)
    rating = models.CharField(max_length=255,null=True)

    class Meta:
        verbose_name = 'Applicant'
        verbose_name_plural = 'Applicants'
        db_table = "applicant_applicants"


