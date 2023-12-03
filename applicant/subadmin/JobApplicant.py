from django.db import models
from django.contrib import admin
from job.models import Job
from applicant.models import JobApplicant
from core.models import User
import requests
from django.core.serializers.json import DjangoJSONEncoder
import json
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from job.utils.utils import sync_jobs_from_api
from applicant.utils.utils import sync_job_applicants_from_api
from django.urls import path
from datetime import datetime
from django.utils.html import format_html


class JobApplicantAdmin(admin.ModelAdmin):
    change_list_template = "applicant/applicant_changelist.html"
    list_display = ['applicant_id','first_name','last_name','prospect_phone','apply_date','job_id','job_title','progress_bar']
    exclude = ['created_on', 'updated_on','ip_address','created_by','updated_by']
   
    def job_id(self, obj):
        if obj:
            return obj.job.job_id
        return ""
   
    def job_title(self, obj):
        if obj:
            return obj.job.title
        return ""

    def progress_bar(self, obj):
        progress = obj.progress  # Replace 'progress' with the actual field name in your model
        return format_html(
            '<progress value="{}" max="100"></progress>'
            '<span> {}%</span>',
          progress, progress
        )
    progress_bar.short_description = 'Progress'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('sync_applicants/', self.sync_applicants, name='sync_applicants'),
        ]
        return my_urls + urls

    def sync_applicants(self,request):
        # Your API call logic here
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
            print("Error:", response.status_code)     # Redirect to the changelist page
        change_list_url = reverse(
            'admin:%s_%s_changelist' % (
                'applicant',
                'jobapplicant',
            ),
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(change_list_url)
   
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # form.base_fields['workflow_id'].initial = 'workflow_1'
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # if db_field.name == "hiring_lead":
        #     kwargs["queryset"] = User.objects.filter(is_superuser=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def save_model(self, request, obj, form, change):
        # Perform the POST request
        url = "https://api.resumatorapi.com/v1/applicants?apikey=MQFrqMaAJP0PH9Q93tyEDDoUWKSvY6xh"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # Process the response data here
            print(data)
        else:
            print("Error:", response.status_code)
        # super().save_model(request, obj, form, change)

admin.site.register(JobApplicant,JobApplicantAdmin)