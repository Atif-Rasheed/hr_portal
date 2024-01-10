from django.contrib import admin
from django.shortcuts import redirect

class MyAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        if request.user.is_authenticated and request.user.type == "hiring_manager":
            return redirect('admin:job_dashboard_changelist')  # Replace with your actual URL pattern name
        context = {
            'custom_variable': 'Hello from the custom admin index!',
        }
        return super().index(request, extra_context=context)
    