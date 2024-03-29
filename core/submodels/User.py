from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100,verbose_name="ID")
    TYPE_CHOICES = (
        ('administrator', 'Administrator'),
        ('hiring_manager', 'Hiring Manager'),
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=1)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    workflow_id = models.CharField(max_length=50, blank=True, null=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username
