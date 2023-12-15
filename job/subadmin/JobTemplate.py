from django.db import models
from django.contrib import admin
from django import forms
from job.models import Job
from core.models import User
import requests
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.urls import reverse
from django.http import HttpResponseRedirect
from job.utils.utils import sync_jobs_from_api
from django.urls import path
from ..models import TestlifyLink,JobTemplate
from ..admin import TestlifyLinkInline


class JobTemplateAdmin(admin.ModelAdmin):
    change_list_template = 'job/job_changelist.html'
    list_display = ['title','job_id','created_by','get_testlify_links']
    exclude = ['created_on', 'updated_on','ip_address','created_by','updated_by','job_id','workflow_id']
    inlines = [TestlifyLinkInline,]
    
    fieldsets = [
        ('Job Information', {'fields': [('title', 'employment_type'),('department','internal_job_code'),'eeo_1_job_category', 'syndication', 'open_date','description']}),
        ('Privacy Information', {'fields': [('confidential', 'private')]}),
        ('Salary Information', {'fields': [('approved_salary_range_minimum', 'approved_salary_range_maximum')]}),
        ('Geo Information', {'fields': [('state', 'city','postal_code')]}),
        ('Canned Fields', {'fields': [('canned_address', 'canned_cover_letter','canned_references'),('canned_wmyu','canned_linked_in','canned_website'),('canned_twitter_username','canned_start','canned_weekends'),('canned_evenings','canned_overtime','canned_languages'),('canned_salary','canned_referral','canned_license'),('canned_cdl','canned_relocate','canned_citizen'),('canned_education','canned_college','canned_gpa'),('canned_over18','canned_flighthours','canned_flightgrade'),('canned_felony','canned_felonyexplain')]}),
    ]

    def get_testlify_links(self, obj):
        # Retrieve and format information from related TestlifyLink instances
        testlify_links = TestlifyLink.objects.filter(job_template=obj)
        return ', '.join(link.link for link in testlify_links)

    get_testlify_links.short_description = 'Testlify Links'

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

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()

admin.site.register(JobTemplate, JobTemplateAdmin)