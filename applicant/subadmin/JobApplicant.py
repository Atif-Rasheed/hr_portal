from django.db import models
from django.contrib import admin
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

class JobApplicantAdmin(admin.ModelAdmin):
    list_display = ['applicant_id','first_name','last_name','prospect_phone','apply_date','job_id','job_title']
    exclude = ['created_on', 'updated_on','ip_address','created_by','updated_by']
    actions = ['sync_job_action']
    def sync_job_action(self, request, queryset):
        # Your API call logic here
        sync_jobs_from_api()
        # Redirect to the current admin page to refresh the page
        change_list_url = reverse(
            'admin:%s_%s_changelist' % (
                queryset.model._meta.app_label,
                queryset.model._meta.model_name,
            ),
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(change_list_url)
    sync_job_action.short_description = 'Sync Job Applicants'
   

    def job_id(self, obj):
        if obj:
            return obj.job.job_id
        return ""
   
    def job_title(self, obj):
        if obj:
            return obj.job.title
        return ""
   
    
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