from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from core.models import User
from django import forms


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class UserAdmin(UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        'user_id',
        *UserAdmin.list_display,  # Include the original list_display fields
        'workflow_id',  # Add your custom field
    )
    fieldsets = (
        *UserAdmin.fieldsets,  # Include the original fieldsets
        ('Custom Fields', {'fields': ('workflow_id','user_id')}),  # Add your custom field
    )
  
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            obj.is_staff = True
            obj.save()
            group, created = Group.objects.get_or_create(name='Hiring Manager')
            obj.groups.add(group)
            obj.save()
        else:
            group, created = Group.objects.get_or_create(name='Hiring Manager')
            print(group)
            obj.groups.add(group)
            obj.save()
            print("ELSE CALLED")

admin.site.register(User, UserAdmin)