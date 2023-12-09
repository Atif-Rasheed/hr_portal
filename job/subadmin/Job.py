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
from ..models import TestlifyLink
from ..admin import TestlifyLinkInline


class JobAdmin(admin.ModelAdmin):
    change_list_template = 'job/job_changelist.html'
    list_display = ['job_id','title','job_status','get_testlify_links']
    exclude = ['created_on', 'updated_on','ip_address','created_by','updated_by','job_id','workflow_id','hiring_lead']
    inlines = [TestlifyLinkInline,]


    def get_testlify_links(self, obj):
        # Retrieve and format information from related TestlifyLink instances
        testlify_links = TestlifyLink.objects.filter(job_template=obj)
        return ', '.join(link.link for link in testlify_links)

    get_testlify_links.short_description = 'Testlify Links'


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
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()

admin.site.register(Job, JobAdmin)