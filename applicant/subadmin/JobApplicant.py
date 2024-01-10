from django.db import models
from django.contrib import admin
from job.models import Job,TestlifyLink
from applicant.models import JobApplicant
from core.models import User,CalendlyLink
import requests
from django.core.serializers.json import DjangoJSONEncoder
import json
from django import forms
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.urls import path
from datetime import datetime
from django.utils.html import format_html
from django.core.mail import send_mail
from job.utils.utils import sync_jobs_from_api
from job.models import Job
from applicant.utils.utils import sync_job_applicants_from_api
from django.views.decorators.csrf import csrf_exempt


class JobApplicantAdmin(admin.ModelAdmin):
    change_list_template = "applicant/applicant_changelist.html"
    change_form_template = 'applicant/applicant_changeform.html'
    list_display = ['first_name','last_name','apply_date','job_title','progress_bar','get_testlify_links','get_checkr_form','schedule_interview']
    # list_filter = ['job',]
    exclude = ['created_on', 'updated_on','ip_address','created_by','updated_by']
   
    def job_id(self, obj):
        if obj:
            return obj.job.job_id
        return ""
   
    def job_title(self, obj):
        if obj:
            return obj.job.title
        return ""
    
    def get_testlify_links(self, obj):
        # Retrieve and format information from related TestlifyLink instances
        testlify_links = TestlifyLink.objects.filter(job_template=obj.job.job_template)
        if testlify_links.exists() and obj.email:
            links = [link.link for link in testlify_links]
            first_name = obj.first_name 
            last_name = obj.last_name 
            email = obj.email 

            link = testlify_links.first().link
            button_html = format_html(
                '<button type="buttton" class="btn btn-success" onclick="sendTestlifyLinks({}, \'{}\', \'{}\',\'{}\')">'
                '<img src="/static/admin/img/icon-addlink.svg" width="16" height="16" alt="Add">'
                'Send Testlify'
                '</button>'.format(links,email,first_name,last_name)
            )
        else:
            button_html = format_html(
                '<button class="btn btn-success" disabled>'
                '<img src="/static/admin/img/icon-addlink.svg" width="16" height="16" alt="Add">'
                'Send Testlify'
                '</button>'
            )
        return button_html

    get_testlify_links.short_description = 'Testlify Links'
    
    def get_checkr_form(self, obj):
        # Retrieve and format information from related TestlifyLink instances
        button_html = format_html('<buttpn type="button" class="btn btn-warning" id="new-invitation-modal-button">'
          '<img src="/static/admin/img/icon-addlink.svg" width="16" height="16" alt="Add">'
          'Background Check'
        '</button>')
        return button_html

    get_checkr_form.short_description = 'Background Check'
    
    def schedule_interview(self, obj):
        first_name = obj.first_name 
        last_name = obj.last_name 
        email = obj.email 
        button_html = format_html(
            '<button type="buttton" class="btn btn-danger" onclick="sendCalendlyLinks(\'{}\', \'{}\',\'{}\')">'
            '<img src="/static/admin/img/icon-addlink.svg" width="16" height="16" alt="Add">'
            'Schedule Interview'
            '</button>'.format(email,first_name,last_name)
        )
        return button_html
    schedule_interview.short_description = 'Schedule Interview'

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
            path('send-testlify-links/', self.send_testlify_links, name='send_testlify_links'),
            path('send-calendly-links/', self.send_calendly_links, name='send_calendly_links'),
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
            data = response.json()
            job_instance = Job.objects.filter(job_id = job_id).first()
           
            if job_instance:
                applicant, created = JobApplicant.objects.get_or_create(applicant_id=applicant_id, defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'prospect_phone': prospect_phone,
                    'apply_date': datetime.strptime(apply_date, '%Y-%m-%d'),
                    'job' : job_instance
                })
                messages.success(request, 'Applicants sync successfully.')
            else:
                messages.warning(request, f'job with id {job_id} not found')

        change_list_url = reverse(
            'admin:%s_%s_changelist' % (
                'applicant',
                'jobapplicant',
            ),
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(change_list_url)

    @csrf_exempt
    def send_testlify_links(self,request):
        if request.method == 'POST':
            links = request.POST.getlist('links[]')
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            applicant_email = request.POST.get('applicantEmail')

            # Send email to the applicant with the links
            subject = 'Your Testlify Links'
            message = f"Dear {first_name} {last_name},\n\nHere are your Testlify links:\n\n"
            for link in links:
                message += f"- {link}\n"
            message += f"\nBest regards,\n {request.user.get_full_name()} from SunRayOps"
            send_mail(subject, message, 'no-reply@sunrayops.com', [applicant_email], fail_silently=False)
            return HttpResponse('Email sent successfully!')
        else:
            return HttpResponse("Failed to send email")
        
    @csrf_exempt
    def send_calendly_links(self,request):
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        applicant_email = request.POST.get('applicantEmail')
        calendly_links = CalendlyLink.objects.filter(hiring_lead=request.user)

        if calendly_links.exists():
            links = [link.link for link in calendly_links]
            # Construct the email content
            subject = 'Calendly Links'
            subject = 'Calendly Invitation Links'
            message = f"Dear {first_name} {last_name},\n\nHere are hiring manager's calendly links:\n\n"
            for link in links:
                message += f"- {link}\n"
            message += f"\nBest regards,\n {request.user.get_full_name()} from SunRayOps"
            from_email = 'no-reply@sunrayops.com'
            to_email = [applicant_email]
            send_mail(subject, message, 'no-reply@sunrayops.com', [applicant_email], fail_silently=False)
            return HttpResponse('Email sent successfully!')
        else:
            return HttpResponse("Failed to send email")
        
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # form.base_fields['workflow_id'].initial = 'workflow_1'
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # if db_field.name == "hiring_lead":
        #     kwargs["queryset"] = User.objects.filter(is_superuser=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()
admin.site.register(JobApplicant,JobApplicantAdmin)