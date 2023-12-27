from django.db import models
from core.models import User
import uuid

class CalendlyLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_calendly_link',null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_calendly_link',null=True)
    ip_address = models.GenericIPAddressField(null=True)
    hiring_lead = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    link = models.URLField(verbose_name="Calendly Link")

    class Meta:
        verbose_name = 'Calendly Link'
        verbose_name_plural = 'Calendly Links'
        db_table = "core_calendly_link"
    
