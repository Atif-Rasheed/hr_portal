from core.models import User
from applicant.models import JobApplicant
from job.models import Job
import requests
from django.utils import timezone
from datetime import datetime
from django.shortcuts import get_object_or_404

def sync_jobs_from_api():
    url = "https://api.resumatorapi.com/v1/jobs?apikey=MQFrqMaAJP0PH9Q93tyEDDoUWKSvY6xh"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        for entry in data:
            title = entry['title']
            hiring_lead = User.objects.filter(user_id=entry['hiring_lead']).first()
            country = entry['country_id']
            description = entry['description']
            workflow_id = '594017'
            job_status = entry['status']
            job_id = entry['id']
            approved_salary_range_minimum = entry['minimum_salary']
            approved_salary_range_maximum = entry['maximum_salary']

            job, created = Job.objects.get_or_create(job_id=job_id, defaults={
                'title': title,
                'hiring_lead': hiring_lead,
                'created_by': hiring_lead,
                'description': description,
                'job_status': job_status,
                'workflow_id': workflow_id,
                'approved_salary_range_minimum': approved_salary_range_minimum,
                'approved_salary_range_maximum': approved_salary_range_maximum,
            })
    else:
        print("Error:", response.status_code)