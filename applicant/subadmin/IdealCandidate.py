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
from applicant.models import IdealCandidate
from applicant.admin import JobApplicantAdmin


class IdealCandidateAdmin(JobApplicantAdmin):
    pass

admin.site.register(IdealCandidate,IdealCandidateAdmin)