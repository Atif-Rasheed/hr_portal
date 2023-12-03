from django.contrib import admin
from ..models import JobTitleTemplate
import json

@admin.register(JobTitleTemplate)
class JobTitleTemplateAdmin(admin.ModelAdmin):
    exclude = ['created_on', 'updated_on','ip_address','created_by','updated_by']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()
