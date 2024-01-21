from django.db import models
from core.models import User
from job.models import Job
from applicant.models import JobApplicant
import uuid

class JobApplicantFeedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="c_%(app_label)s_%(class)ss",null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="u_%(app_label)s_%(class)ss",null=True)
    ip_address = models.GenericIPAddressField(null=True)
    applicant = models.ForeignKey(JobApplicant, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)ss", null=True)
    feedback = models.TextField()
    
    def __str__(self):
        return f"Feedback for {self.applicant.name}"

    class Meta:
        verbose_name = 'Applicant Feedback'
        verbose_name_plural = 'Applicant Feedbacks'
        db_table = "applicant_applicant_feedbacks"


