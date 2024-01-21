from django.db import models
from django.contrib import admin
from job.models import Job,TestlifyLink
from applicant.models import JobApplicant,JobApplicantComment,JobApplicantFeedback,JobApplicantActivity,JobApplicantMessage,JobApplicantAppliedJob
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
from datetime import datetime
from django.conf import settings
from decimal import Decimal
from applicant.utils.JobApplicantManager import JobApplicantManager,JobApplicantAppliedJob


class JobApplicantAdmin(admin.ModelAdmin):
    change_list_template = "applicant/applicant_changelist.html"
    change_form_template = 'applicant/applicant_changeform.html'
    list_display = ['first_name','last_name','email','apply_date','progress_bar','job_id','get_testlify_links','get_checkr_form','schedule_interview']
    list_per_page = 20
    list_filter = ['applicant_jobapplicantappliedjobs__job',]
    exclude = ['created_on', 'updated_on','ip_address','created_by','updated_by']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if extra_context is None:
            extra_context = {}
        extra_context['applied_job'] = JobApplicantAppliedJob.objects.filter(applicant_id=obj.id).first()
        return super().change_view(request, object_id, form_url, extra_context)

   
    def job_id(self, obj):
        if obj:
            applied_job = JobApplicantAppliedJob.objects.filter(applicant = obj).first()
            if applied_job:
                return applied_job.job.job_id
            else:
                return ""
        return ""
   
    def get_testlify_links(self, obj):
        # Retrieve and format information from related TestlifyLink instances
        applied_job = JobApplicantAppliedJob.objects.filter(applicant = obj).first()
        if applied_job:
            testlify_links = TestlifyLink.objects.filter(job_template=applied_job.job.job_template)
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
        applied_job = JobApplicantAppliedJob.objects.filter(applicant = obj).first()
        if applied_job:
            return applied_job.applicant_progress
        else:
            return "No Progress Found"
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
        API_KEY = getattr(settings, 'API_KEY')
        # Your API call logic here
        url = f"https://api.resumatorapi.com/v1/applicants?apikey={API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            applicants_data = response.json()
            # Process the response data here
            for data in applicants_data:
                applicant_id = data['id']
                if applicant_id:
                    url = f"https://api.resumatorapi.com/v1/applicants/{applicant_id}?apikey={API_KEY}"
                    response = requests.get(url)
                    if response.status_code == 200:
                        applicant_detail_data = response.json()
                        applicant = JobApplicant.objects.filter(applicant_id = applicant_id).first()
                        if applicant is None:
                            applicant = JobApplicant()
                        applicant.applicant_id = applicant_id
                        applicant.first_name = applicant_detail_data['first_name']
                        applicant.last_name = applicant_detail_data['last_name']
                        applicant.email = applicant_detail_data['email']
                        applicant.address = applicant_detail_data['address']
                        applicant.location = applicant_detail_data['location']
                        applicant.prospect_phone = applicant_detail_data['phone']
                        applicant.linkedin_url = applicant_detail_data['linkedin_url']
                        applicant.eeo_gender = applicant_detail_data['eeo_gender']
                        applicant.eeo_race = applicant_detail_data['eeo_race']
                        applicant.eeo_disability = applicant_detail_data['eeo_disability']
                        applicant.website = applicant_detail_data['website']
                        if applicant_detail_data['desired_salary']:
                            applicant.college_gpa = Decimal(applicant_detail_data['desired_salary'])
                        if applicant_detail_data['desired_start_date']:
                            desired_start_date = datetime.strptime(applicant_detail_data['desired_start_date'], "%Y-%m-%d").date()
                            applicant.desired_start_date = desired_start_date
                        applicant.languages = applicant_detail_data['languages']
                        applicant.wmyu = applicant_detail_data['wmyu']
                        applicant.has_driver_license = applicant_detail_data['has_driver_license']
                        applicant.willing_to_relocate = applicant_detail_data['willing_to_relocate']
                        applicant.citizenship_status = applicant_detail_data['citizenship_status']
                        applicant.education_level = applicant_detail_data['education_level']
                        applicant.has_cdl = applicant_detail_data['has_cdl']
                        applicant.over_18 = applicant_detail_data['over_18']
                        applicant.can_work_weekends = applicant_detail_data['can_work_weekends']
                        applicant.can_work_evenings = applicant_detail_data['can_work_evenings']
                        applicant.can_work_overtime = applicant_detail_data['can_work_overtime']
                        applicant.has_felony = applicant_detail_data['has_felony']
                        applicant.felony_explanation = applicant_detail_data['felony_explanation']
                        applicant.twitter_username = applicant_detail_data['twitter_username']
                        if applicant_detail_data['college_gpa']:
                            applicant.college_gpa = Decimal(applicant_detail_data['college_gpa'])
                        applicant.college = applicant_detail_data['college']
                        applicant.references = applicant_detail_data['references']
                        applicant.notes = applicant_detail_data['notes']
                        if applicant_detail_data['apply_date']:
                            apply_date = datetime.strptime(applicant_detail_data['apply_date'], "%Y-%m-%d").date()
                            applicant.apply_date = apply_date
                        applicant.comments_count = applicant_detail_data['comments_count']                         
                        applicant.source = applicant_detail_data['source']                         
                        if applicant_detail_data['eeoc_veteran']:   
                            applicant.eeoc_veteran = applicant_detail_data['eeoc_veteran']                         
                        if applicant_detail_data['eeoc_disability']:   
                            applicant.eeoc_disability = applicant_detail_data['eeoc_disability']                         
                        if applicant_detail_data['eeoc_disability_signature']:   
                            applicant.eeoc_disability_signature = applicant_detail_data['eeoc_disability_signature']                         
                        if applicant_detail_data['eeoc_disability_date']:
                            eeoc_disability_date = datetime.strptime(applicant_detail_data['eeoc_disability_date'], "%Y-%m-%d").date()
                            applicant.eeoc_disability_date = eeoc_disability_date
                        if "resume_link" in applicant_detail_data:                       
                            applicant.resume_link = applicant_detail_data['resume_link']
                        applicant.save()
                        
                        # Applicant Related Data
                        applicant_manager = JobApplicantManager(applicant)
                        
                        # Delete existing comments for the applicant
                        JobApplicantComment.objects.filter(applicant=applicant).delete()
                        # Add new comments
                        if 'comments' in applicant_detail_data and applicant_detail_data['comments']:
                            if isinstance(applicant_detail_data['comments'], list):
                                for comment in applicant_detail_data['comments']:
                                    applicant_manager.create_job_applicant_comment(comment)
                            else:
                                comment = applicant_detail_data['comments']
                                applicant_manager.create_job_applicant_feedback(comment)
                        
                        # Delete existing feedbacks for the applicant
                        JobApplicantFeedback.objects.filter(applicant=applicant).delete()
                        # Add new activities
                        if 'feedbacks' in applicant_detail_data and applicant_detail_data['feedbacks']:
                            if isinstance(applicant_detail_data['feedbacks'], list):
                                for feedback in applicant_detail_data['feedbacks']:
                                    applicant_manager.create_job_applicant_feedback(feedback)
                            else:
                                feedback = applicant_detail_data['feedbacks']
                                applicant_manager.create_job_applicant_feedback(feedback)
                        
                        # Delete existing activities for the applicant
                        JobApplicantActivity.objects.filter(applicant=applicant).delete()
                        # Add new activities
                        if 'activites' in applicant_detail_data and applicant_detail_data['activites']:
                            if isinstance(applicant_detail_data['activites'], list):
                                for activity in applicant_detail_data['activites']:
                                    applicant_manager.create_applicant_activity(activity)
                            else:
                                activity = applicant_detail_data['messages']
                                applicant_manager.create_applicant_activity(activity)

                        
                        # Delete existing messages for the applicant
                        JobApplicantMessage.objects.filter(applicant=applicant).delete()
                        # Add new messages
                        if 'messages' in applicant_detail_data and applicant_detail_data['messages']:
                            if isinstance(applicant_detail_data['messages'], list):
                                for message in applicant_detail_data['messages']:
                                    applicant_manager.create_job_applicant_message(message)
                            else:
                                message = applicant_detail_data['messages']
                                applicant_manager.create_job_applicant_message(message)
                        

                        # Delete existing messages for the applicant
                        JobApplicantAppliedJob.objects.filter(applicant=applicant).delete()
                        # Add new messages
                        if 'jobs' in applicant_detail_data and applicant_detail_data['jobs']:
                            if isinstance(applicant_detail_data['jobs'], list):
                                for job in applicant_detail_data['jobs']:
                                    applicant_manager.create_applicant_applied_job(job)
                            else:
                                job = applicant_detail_data['jobs']
                                applicant_manager.create_applicant_applied_job(job)

            messages.success(request, f'Applicants sync successfully.')
           

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