from django.db import models
from django.contrib import admin
from job.models import News
from core.models import User
import requests
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.urls import reverse
from django.http import HttpResponseRedirect
from job.utils.utils import sync_jobs_from_api


class NewsAdmin(admin.ModelAdmin):
    change_list_template = "job/news_changelist.html"    

    def has_add_permission(self, request):
        return not request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return not request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return not request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return not request.user.is_superuser


admin.site.register(News, NewsAdmin)