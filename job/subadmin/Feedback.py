from django.contrib import admin
from ..models import Feedback
import json

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    exclude = ['created_on', 'updated_on','ip_address','created_by','updated_by']

    def has_add_permission(self, request):
        return not request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return not request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return not request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return not request.user.is_superuser


    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()
