from core.models import User
from applicant.models import JobApplicant
from job.models import Job,JobTemplate
import requests
from django.utils import timezone
from datetime import datetime
from django.shortcuts import get_object_or_404
from hr_portal.settings import API_KEY

def get_status_code(status):
    job_status_choices = {
        "Open (default)": "1",
        "On Hold": "3",
        "Approved": "8",
        "Needs Approval": "7",
        "Drafting": "2",
        "Filled": "4",
        "Canceled": "5",
        "Closed": "6",
    }

    # Default to "1" if the status is not found in the choices
    return job_status_choices.get(status, "1")

def get_employment_type_code(employment_type):
    employment_type_choices = {
        'Full Time': '1',
        'Part Time': '2',
        'Part Time to Full Time': '3',
        'Temporary': '4',
        'Temporary to Full Time': '5',
        'Contracted': '6',
        'Contracted to Full Time': '7',
        'Internship': '8',
        'Internship to Full Time': '9',
        'Volunteer': '10',
        'Seasonal': '11',
    }

    # Default to "1" if the employment type is not found in the choices
    return employment_type_choices.get(employment_type, '1')


def sync_jobs_from_api(request):
    url = f"https://api.resumatorapi.com/v1/jobs?apikey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        for entry in data:
            job_id = entry['id']
            title = entry['title']
            hiring_lead = User.objects.filter(user_id=entry['hiring_lead']).first()
            country = entry['country_id']
            city = entry['city']
            state = entry['state']
            zip = entry['zip']
            department = entry['department']
            description = entry['description']
            minimum_salary = entry['minimum_salary']
            maximum_salary = entry['maximum_salary']
            notes = entry['notes']
            original_open_date = entry['original_open_date']
            type = entry['type']
            status = entry['status']
            internal_code = entry['internal_code']
            
            job_template = JobTemplate.objects.filter(title = title).first()
            if job_template is None:
                if request.user.is_superuser:
                    job_template, created = JobTemplate.objects.get_or_create(job_id=job_id, defaults={
                        'job_id':job_id,
                        'title': title,
                        'city':city,
                        'state':state,
                        'department':department,
                        'description':description,
                        'approved_salary_range_minimum': minimum_salary,
                        'approved_salary_range_maximum': maximum_salary,
                        'open_date':original_open_date,
                        'employment_type': get_employment_type_code(type),
                        'internal_job_code':internal_code,
                        'created_by': hiring_lead,
                        'job_status': get_status_code(status),
                    })
                else:
                    return f"{title} Template do not exist"

            if job_template:
                job, created = Job.objects.get_or_create(job_id=job_id, defaults={
                    'job_id':job_id,
                    'title': title,
                    'job_template':job_template,
                    'country':country,
                    'city':city,
                    'state':state,
                    'department':department,
                    'description':description,
                    'approved_salary_range_minimum': minimum_salary,
                    'approved_salary_range_maximum': maximum_salary,
                    'open_date':original_open_date,
                    'employment_type': get_employment_type_code(type),
                    'internal_job_code':internal_code,
                    'hiring_lead': hiring_lead,
                    'created_by': hiring_lead,
                    'job_status': get_status_code(status),
                })
                print(job,created)
               
    else:
        print("Error:", response.status_code)


def create_new_job(request,job_instance):
    url = "https://api.resumatorapi.com/v1/jobs"

    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "apikey": "MQFrqMaAJP0PH9Q93tyEDDoUWKSvY6xh",
        "job_status":1,
        "country": 61,
        "title": job_instance.title,
        "hiring_lead_id": str(job_instance.hiring_lead.user_id),
        'title': job_instance.title,
        'description': job_instance.job_template.description,
        'workflow_id': request.user.workflow_id,
        'job_id': job_instance.job_id,
        'employment_type': job_instance.employment_type,
        'minimum_experience': job_instance.minimum_experience,
        'confidential': job_instance.confidential,
        'private': job_instance.private,
        'canned_address': job_instance.canned_address,
        'canned_cover_letter': job_instance.canned_cover_letter,
        'canned_references': job_instance.canned_references,
        'canned_wmyu': job_instance.canned_wmyu,
        'canned_linked_in': job_instance.canned_linked_in,
        'canned_website': job_instance.canned_website,
        'canned_twitter_username': job_instance.canned_twitter_username,
        'canned_start': job_instance.canned_start,
        'canned_weekends': job_instance.canned_weekends,
        'canned_evenings': job_instance.canned_evenings,
        'canned_overtime': job_instance.canned_overtime,
        'canned_languages': job_instance.canned_languages,
        'canned_salary': job_instance.canned_salary,
        'canned_referral': job_instance.canned_referral,
        'canned_license': job_instance.canned_license,
        'canned_cdl': job_instance.canned_cdl,
        'canned_relocate': job_instance.canned_relocate,
        'canned_citizen': job_instance.canned_citizen,
        'canned_education': job_instance.canned_education,
        'canned_college': job_instance.canned_college,
        'canned_over18': job_instance.canned_over18,
        'canned_flighthours': job_instance.canned_flighthours,
        'canned_flightgrade': job_instance.canned_flightgrade,
        'canned_felony': job_instance.canned_felony,
        'canned_felonyexplain': job_instance.canned_felonyexplain,
        'approved_salary_range_minimum': str(job_instance.approved_salary_range_minimum),
        'approved_salary_range_maximum': str(job_instance.approved_salary_range_maximum),
        'department': job_instance.department,
        'state': job_instance.state,
        'city': job_instance.city,
        'postal_code': job_instance.postal_code,
        'internal_job_code': job_instance.internal_job_code,
        'eeo_1_job_category': job_instance.eeo_1_job_category,
        'syndication': job_instance.syndication,
        'open_date': str(job_instance.open_date)
    }

    response = requests.post(url, headers=headers, json=data)

    # Check the response
    if response.status_code == 201:  # Assuming a successful response has status code 201 (Created)
        print("Job created successfully.")
    else:
        print(f"Failed to create job. Status code: {response.status_code}, Response: {response.text}")