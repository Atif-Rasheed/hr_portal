from django.db import models
from django.contrib import admin
from job.models import Job,Dashboard
from applicant.models import JobApplicant
from core.models import User
from django.urls import reverse
from django.shortcuts import redirect


class DashboardAdmin(admin.ModelAdmin):
    change_list_template = "job/dashboard_changelist.html"

    def has_add_permission(self, request):
        return not request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return not request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return not request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return not request.user.is_superuser


    def changelist_view(self, request, extra_context=None):
        job_qs = Job.objects.all()
        applicant_qs = JobApplicant.objects.all()
        # Pass the queryset as context
        extra_context = extra_context or {}
        extra_context['job_queryset'] = job_qs
        extra_context['applicant_queryset'] = applicant_qs

        return super().changelist_view(request, extra_context=extra_context)    

admin.site.register(Dashboard, DashboardAdmin)