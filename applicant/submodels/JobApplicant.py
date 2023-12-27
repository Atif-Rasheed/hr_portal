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
    apply_date = models.DateField(auto_now_add=True)
    current_position = models.CharField(max_length=255,null=True)
    start_date = models.DateField(null=True)
    status = models.CharField(max_length=255,null=True,blank=True)
    rating = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(max_length=254, unique=True,null=True)
    progress = models.PositiveIntegerField(default=0, null= True,blank=True)

    @property
    def progress(self):
        # if self.total_tasks == 0:
        #     return 0
        # return (self.completed_tasks / self.total_tasks) * 100
        return 50
    
    def save(self, *args, **kwargs):
        self.progress_bar = self.progress
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = 'Applicant'
        verbose_name_plural = 'Applicants'
        db_table = "applicant_applicants"


