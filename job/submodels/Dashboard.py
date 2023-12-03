from django.db import models
from job.models import Job

class CustomDashboardManager(models.Manager):
    def get_queryset(self):
        # Customize the queryset if needed
        return super().get_queryset()

class Dashboard(Job):
    objects = CustomDashboardManager()

    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = "Dashboard"

    def custom_method(self):
        # Add custom methods or override existing ones
        pass