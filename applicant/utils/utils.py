from core.models import User
from applicant.models import JobApplicant
from job.models import Job
import requests
from django.utils import timezone
from datetime import datetime
from django.shortcuts import get_object_or_404

def sync_job_applicants_from_api():
        url = "https://api.resumatorapi.com/v1/applicants?apikey=MQFrqMaAJP0PH9Q93tyEDDoUWKSvY6xh"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # Process the response data here
            applicant_id = data['id']
            first_name = data['first_name']
            last_name = data['last_name']
            prospect_phone = data['prospect_phone']
            apply_date = data['apply_date']
            job_id = data['job_id']
            job_instance = Job.objects.filter(job_id = job_id).first()
            
            applicant, created = JobApplicant.objects.get_or_create(applicant_id=applicant_id, defaults={
                'first_name': first_name,
                'last_name': last_name,
                'prospect_phone': prospect_phone,
                'apply_date': datetime.strptime(apply_date, '%Y-%m-%d'),
                'job' : job_instance
            })

        else:
            print("Error:", response.status_code)