from django.db import models
from applicant.models import JobApplicant

class CustomIdealCandidateManager(models.Manager):
    def get_queryset(self):
        # Customize the queryset if needed
        return super().get_queryset()

class IdealCandidate(JobApplicant):
    objects = CustomIdealCandidateManager()

    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = "Ideal Candidates"

    