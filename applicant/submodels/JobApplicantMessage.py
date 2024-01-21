from django.db import models
from core.models import User
from job.models import Job
from applicant.models import JobApplicant
import uuid

class JobApplicantMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="c_%(app_label)s_%(class)ss",null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="u_%(app_label)s_%(class)ss",null=True)
    ip_address = models.GenericIPAddressField(null=True)
    applicant = models.ForeignKey(JobApplicant, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)ss", null=True)
    comm_id = models.CharField(max_length=255)
    comm_subject = models.CharField(max_length=255)
    comm_text = models.TextField()
    comm_author_email = models.EmailField()
    comm_to = models.EmailField()
    comm_cc = models.EmailField(blank=True, null=True)
    comm_bcc = models.EmailField(blank=True, null=True)
    comm_datetime_sent = models.DateTimeField()
    
    def __str__(self):
        return f"{self.comm_subject} for {self.applicant.full_name}"

    class Meta:
        verbose_name = 'Applicant Communication'
        verbose_name_plural = 'Applicant Communications'
        db_table = "applicant_applicant_communications"


