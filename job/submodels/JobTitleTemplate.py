from django.db import models
from core.models import User
import uuid

class JobTitleTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_job_title_template')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_job_title_template',null=True)
    ip_address = models.GenericIPAddressField(null=True)
    description = models.TextField()
    skills = models.TextField()
    suggested_experience = models.CharField(max_length=50)
    suggested_minimum_education = models.CharField(max_length=50)

    def __str__(self):
        return self.description