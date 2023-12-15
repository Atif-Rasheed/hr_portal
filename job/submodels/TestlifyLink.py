from django.db import models
from core.models import User
from job.models import JobTemplate
import uuid

class TestlifyLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_testlify_link',null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_testlify_link',null=True)
    ip_address = models.GenericIPAddressField(null=True)
    job_template = models.ForeignKey(JobTemplate, on_delete=models.CASCADE, related_name='testlify_links')
    link = models.URLField(verbose_name="Job Link")

    class Meta:
        verbose_name = 'Testlify Link'
        verbose_name_plural = 'Testlify Links'
        db_table = "job_testlify_link"
    
