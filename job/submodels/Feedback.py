from django.db import models
import uuid
from core.models import User

class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_feedback')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_feedback',null=True)
    ip_address = models.GenericIPAddressField(null=True)
    APPLICANT_QUALITY_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]

    ease_of_use = models.CharField(max_length=10, choices=APPLICANT_QUALITY_CHOICES)
    features = models.CharField(max_length=10, choices=APPLICANT_QUALITY_CHOICES)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback {self.id}"