from django.db import models
from django.contrib import admin
from job.models import Job,JobTemplate,TestlifyLink
from core.models import User
import requests
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.urls import reverse
from django.http import HttpResponseRedirect
from job.utils.utils import sync_jobs_from_api,create_new_job
from django.urls import path
from django.http import JsonResponse
from django.contrib import messages

class JobAdmin(admin.ModelAdmin):
    change_list_template = 'job/job_changelist.html'
    change_form_template = 'job/job_changeform.html'
    list_display = ['job_template','hiring_lead','employment_type','open_date','description','approved_salary_range_minimum','approved_salary_range_maximum','get_testlify_links']
    exclude = ['created_on', 'updated_on','ip_address','created_by','updated_by','job_id','workflow_id','hiring_lead']

    fieldsets = [
        ('Job Information', {'fields': ['job_template',('title', 'employment_type'),('department','internal_job_code'),'eeo_1_job_category', 'syndication', 'open_date','description']}),
        ('Privacy Information', {'fields': [('confidential', 'private')]}),
        ('Salary Information', {'fields': [('approved_salary_range_minimum', 'approved_salary_range_maximum')]}),
        ('Geo Information', {'fields': [('country','state', 'city','postal_code')]}),
        ('Canned Fields', {'fields': [('canned_address', 'canned_cover_letter','canned_references'),('canned_wmyu','canned_linked_in','canned_website'),('canned_twitter_username','canned_start','canned_weekends'),('canned_evenings','canned_overtime','canned_languages'),('canned_salary','canned_referral','canned_license'),('canned_cdl','canned_relocate','canned_citizen'),('canned_education','canned_college','canned_gpa'),('canned_over18','canned_flighthours','canned_flightgrade'),('canned_felony','canned_felonyexplain')]}),
    ]

    def get_testlify_links(self, obj):
        # Retrieve and format information from related TestlifyLink instances
        testlify_links = TestlifyLink.objects.filter(job_template=obj.job_template)
        return ', '.join(link.link for link in testlify_links)

    get_testlify_links.short_description = 'Testlify Links'


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "hiring_lead":
            kwargs["queryset"] = User.objects.filter(is_superuser=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('sync_jobs/', self.sync_jobs, name='sync_jobs'),
            path('get_template_data/', self.admin_site.admin_view(self.get_template_data),name='get_template_data'),
        ]
        return my_urls + urls


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Filter records where the hiring_manager is the current user
        return qs.filter(hiring_lead__user_id=request.user.user_id)


    def sync_jobs(self,request):
        sync_jobs_from_api(request)
        messages.success(request, 'Jobs synchronized successfully.')

        change_list_url = reverse(
            'admin:%s_%s_changelist' % (
                'job',
                'job',
            ),
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(change_list_url)
    
    def get_template_data(self, request):
        template_id = request.GET.get('template_id')
        template = JobTemplate.objects.get(id=template_id)
        data = {
            'title': template.title,
            'description': template.description,
            'job_id': template.job_id,
            'employment_type': template.employment_type,
            'minimum_experience': template.minimum_experience,
            'confidential': template.confidential,
            'private': template.private,
            'canned_address': template.canned_address,
            'canned_cover_letter': template.canned_cover_letter,
            'canned_references': template.canned_references,
            'canned_wmyu': template.canned_wmyu,
            'canned_linked_in': template.canned_linked_in,
            'canned_website': template.canned_website,
            'canned_twitter_username': template.canned_twitter_username,
            'canned_start': template.canned_start,
            'canned_weekends': template.canned_weekends,
            'canned_evenings': template.canned_evenings,
            'canned_overtime': template.canned_overtime,
            'canned_languages': template.canned_languages,
            'canned_salary': template.canned_salary,
            'canned_referral': template.canned_referral,
            'canned_license': template.canned_license,
            'canned_cdl': template.canned_cdl,
            'canned_relocate': template.canned_relocate,
            'canned_citizen': template.canned_citizen,
            'canned_education': template.canned_education,
            'canned_college': template.canned_college,
            'canned_over18': template.canned_over18,
            'canned_flighthours': template.canned_flighthours,
            'canned_flightgrade': template.canned_flightgrade,
            'canned_felony': template.canned_felony,
            'canned_felonyexplain': template.canned_felonyexplain,
            'approved_salary_range_minimum': template.approved_salary_range_minimum,
            'approved_salary_range_maximum': template.approved_salary_range_maximum,
            'department': template.department,
            'state': template.state,
            'city': template.city,
            'postal_code': template.postal_code,
            'internal_job_code': template.internal_job_code,
            'eeo_1_job_category': template.eeo_1_job_category,
            'syndication': template.syndication,
            'open_date': template.open_date
        }
        return JsonResponse(data)
   
    def save_model(self, request, obj, form, change):
        if request.user.workflow_id:
            obj.hiring_lead = request.user
            if not change:
                obj.created_by = request.user
                # Creating New Job
                create_new_job(request,obj)
            else:
                obj.updated_by = request.user
            obj.save()

admin.site.register(Job, JobAdmin)