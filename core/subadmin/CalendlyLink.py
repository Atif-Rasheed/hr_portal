from django.contrib import admin
from ..models import CalendlyLink

class CalendlyLinkInline(admin.StackedInline):
    model = CalendlyLink
    fk_name = 'hiring_lead' 
    extra = 0

    exclude = ['created_by','updated_by','ip_address']

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user

        # Ensure created_by is set before saving
        if change and not obj.created_by:
            obj.created_by = request.user

        obj.updated_by = request.user
        super().save_model(request, obj, form, change)