from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from core.models import User
from applicant.models import JobApplicant
from job.models import Job
import requests
from django.utils import timezone
from datetime import datetime
from django.shortcuts import get_object_or_404
from job.utils.utils import sync_jobs_from_api

class Command(BaseCommand):
    help = 'Create a user with the applicant_admin role if it does not exist'
       
    def handle(self, *args, **options):
       sync_jobs_from_api()