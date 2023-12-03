from django.db import models
from django.contrib import admin
from job.models import Job
from core.models import User
import requests
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.urls import reverse
from django.http import HttpResponseRedirect
from job.utils.utils import sync_jobs_from_api
from django.urls import path


class JobAdmin(admin.ModelAdmin):
    change_list_template = 'job/job_changelist.html'
    list_display = ['job_id','title','job_status']
    exclude = ['created_on', 'updated_on','ip_address','created_by','updated_by','job_id','workflow_id','hiring_lead']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "hiring_lead":
            kwargs["queryset"] = User.objects.filter(is_superuser=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('sync_applicants/', self.sync_jobs, name='sync_jobs'),
        ]
        return my_urls + urls


    def sync_jobs(self,request):
        # Your API call logic here
        sync_jobs_from_api()
        # Redirect to the current admin page to refresh the page
        change_list_url = reverse(
            'admin:%s_%s_changelist' % (
                'job',
                'job',
            ),
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(change_list_url)
   



















    def save_model(self, request, obj, form, change):
        # Perform the POST request
        payload = {}
        payload['title'] = obj.title
        payload['apikey'] = "MQFrqMaAJP0PH9Q93tyEDDoUWKSvY6xh"
        payload['hiring_lead_id'] =  request.user.user_id
        payload['employment_type'] = 1
        payload['country'] = 1
        payload['description'] = obj.description
        payload['workflow_id'] = request.user.workflow_id
        payload['job_status'] = obj.job_status
        payload['canned_felony'] = obj.canned_felony
        payload['canned_education'] = obj.canned_education
        payload['minimum_experience'] = obj.minimum_experience
        payload['approved_salary_range_minimum'] = str(obj.approved_salary_range_minimum)
        payload['approved_salary_range_maximum'] = str(obj.approved_salary_range_maximum)

        url = 'https://api.resumatorapi.com/v1/jobs'

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url,headers=headers,json=payload)
        # Check if the response status code is 200
        if response.status_code == 200:
            json_data = response.json()
            if 'job_id' in json_data:
                if request.user.workflow_id:
                    if not change:
                        obj.created_by = request.user
                    else:
                        obj.updated_by = request.user
                    obj.job_id = json_data['job_id']
                    obj.workflow_id = request.user.workflow_id
                    obj.save()
            else:
                # Now you can work with the JSON data
                print(json_data)
        else:
            # Handle the case when the response status code is not 200
            print(f"Error: {response.status_code}")
            print(response.text)  # Print the response content for debugging

admin.site.register(Job, JobAdmin)