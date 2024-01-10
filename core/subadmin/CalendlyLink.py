from django.contrib import admin
from ..models import CalendlyLink

class CalendlyLinkAdmin(admin.ModelAdmin):
    list_display = ['hiring_lead','link','created_on']
    exclude = ['created_by','updated_by','ip_address']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(hiring_lead=request.user)
        return queryset

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user

        # Ensure created_by is set before saving
        if change and not obj.created_by:
            obj.created_by = request.user

        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(CalendlyLink, CalendlyLinkAdmin)