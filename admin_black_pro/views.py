from django.shortcuts import render, redirect
from admin_black_pro.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeDoneView
from django.contrib.auth import logout,get_user_model
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.send_email import send_email


def dashboard(request):
  context = {
    'segment': 'dashboard'
  }
  return render(request, 'pages/dashboard.html', context)

@login_required(login_url='/accounts/login/')
def widgets(request):
  context = {
    'segment': 'widgets'
  }
  return render(request, 'pages/widgets.html', context)

@login_required(login_url='/accounts/login/')
def charts(request):
  context = {
    'segment': 'charts'
  }
  return render(request, 'pages/charts.html', context)

@login_required(login_url='/accounts/login/')
def calendar(request):
  context = {
    'segment': 'calendar'
  }
  return render(request, 'pages/calendar.html', context)

def templates(request):
  context = {}
  return render(request, 'pages/template.html', context)

# Components
@login_required(login_url='/accounts/login/')
def buttons(request):
  context = {
    'parent': 'components',
    'segment': 'buttons'
  }
  return render(request, 'pages/components/buttons.html', context)

@login_required(login_url='/accounts/login/')
def grid(request):
  context = {
    'parent': 'components',
    'segment': 'grid_system'
  }
  return render(request, 'pages/components/grid.html', context)

@login_required(login_url='/accounts/login/')
def panels(request):
  context = {
    'parent': 'components',
    'segment': 'panels'
  }
  return render(request, 'pages/components/panels.html', context)

@login_required(login_url='/accounts/login/')
def sweet_alert(request):
  context = {
    'parent': 'components',
    'segment': 'sweet_alert'
  }
  return render(request, 'pages/components/sweet-alert.html', context)

@login_required(login_url='/accounts/login/')
def notifications(request):
  context = {
    'parent': 'components',
    'segment': 'notifications'
  }
  return render(request, 'pages/components/notifications.html', context)

@login_required(login_url='/accounts/login/')
def icons(request):
  context = {
    'parent': 'components',
    'segment': 'icons'
  }
  return render(request, 'pages/components/icons.html', context)

@login_required(login_url='/accounts/login/')
def typography(request):
  context = {
    'parent': 'components',
    'segment': 'typography'
  }
  return render(request, 'pages/components/typography.html', context)

# Forms
@login_required(login_url='/accounts/login/')
def regular_forms(request):
  context = {
    'parent': 'forms',
    'segment': 'regular_forms'
  }
  return render(request, 'pages/forms/regular.html', context)

@login_required(login_url='/accounts/login/')
def extended_forms(request):
  context = {
    'parent': 'forms',
    'segment': 'extended_forms'
  }
  return render(request, 'pages/forms/extended.html', context)

@login_required(login_url='/accounts/login/')
def validation_forms(request):
  context = {
    'parent': 'forms',
    'segment': 'validation_forms'
  }
  return render(request, 'pages/forms/validation.html', context)

@login_required(login_url='/accounts/login/')
def wizard(request):
  context = {
    'parent': 'forms',
    'segment': 'wizard'
  }
  return render(request, 'pages/forms/wizard.html', context)

# Tables
@login_required(login_url='/accounts/login/')
def regular_tables(request):
  context = {
    'parent': 'tables',
    'segment': 'regular_tables'
  }
  return render(request, 'pages/tables/regular.html', context)

@login_required(login_url='/accounts/login/')
def extended_tables(request):
  context = {
    'parent': 'tables',
    'segment': 'extended_tables'
  }
  return render(request, 'pages/tables/extended.html', context)

@login_required(login_url='/accounts/login/')
def datatables(request):
  context = {
    'parent': 'tables',
    'segment': 'datatables.net'
  }
  return render(request, 'pages/tables/datatables.net.html', context)

# Maps
@login_required(login_url='/accounts/login/')
def google_maps(request):
  context = {
    'parent': 'maps',
    'segment': 'google_maps'
  }
  return render(request, 'pages/maps/google.html', context)

@login_required(login_url='/accounts/login/')
def fullscreen_map(request):
  context = {
    'parent': 'maps',
    'segment': 'full_screen_map'
  }
  return render(request, 'pages/maps/fullscreen.html', context)

@login_required(login_url='/accounts/login/')
def vector_map(request):
  context = {
    'parent': 'maps',
    'segment': 'vector_map'
  }
  return render(request, 'pages/maps/vector.html', context)

# Pages
@login_required(login_url='/accounts/login/')
def pricing(request):
  context = {
    'segment': 'pricing_page'
  }
  return render(request, 'pages/pages/pricing.html', context)

@login_required(login_url='/accounts/login/')
def timeline(request):
  context = {
    'parent': 'pages',
    'segment': 'timeline'
  }
  return render(request, 'pages/pages/timeline.html', context)

@login_required(login_url='/accounts/login/')
def user_profile(request):
  context = {
    'parent': 'pages',
    'segment': 'user_profile'
  }
  return render(request, 'pages/pages/user.html', context)

@login_required(login_url='/accounts/login/')
def rtl(request):
  return render(request, 'pages/pages/rtl.html')

# Authentication
class UserLoginView(LoginView):
  form_class = LoginForm
  template_name = 'accounts/login.html'
  success_url = '/admin/job/dashboard/'  # Set the success URL to the base URL
  
  def get_context_data(self, *args, **kwargs):
    context = super(UserLoginView, self).get_context_data(*args, **kwargs)
    context['segment'] = 'login_page'
    return context

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Admin User
            User = get_user_model()
            admin_user = User.objects.filter(email="adam@sunrayops.com").first()

            if admin_user:
                user.user_id = admin_user.user_id
                user.is_staff = True
                user.is_superuser = False
                user.type = 'hiring_manager'
                user.save()
                group, created = Group.objects.get_or_create(name='Hiring Manager')
                user.groups.add(group)
                user.save()

                # Sending Email Notification To Superuser
                send_email(subject="Hiring Manager Registration",body=f"{user.full_name} is registered as hiring manager at {user.date_joined}",recipient_email=user.email)
                print("Account created successfully!")
                return redirect('/accounts/login/')
            else:
                # Display a message indicating that the admin user does not exist
                messages.error(request, "Unable to register. Administrator does not exist.")
                print("Registration failed!")
        else:
            print("Registration failed!")
    else:
        form = RegistrationForm()

    context = {
        'segment': 'register_page',
        'form': form
    }
    return render(request, 'accounts/register.html', context)

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password-reset.html'
  form_class = UserPasswordResetForm

  def get_context_data(self, *args, **kwargs):
    context = super(UserPasswordResetView, self).get_context_data(*args, **kwargs)
    context['segment'] = 'password_reset_page'
    return context

class UserPasswrodResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/reset-confirm.html'
  form_class = UserSetPasswordForm

  def get_context_data(self, *args, **kwargs):
    context = super(UserPasswrodResetConfirmView, self).get_context_data(*args, **kwargs)
    context['segment'] = 'reset_confirm_page'
    return context


class UserPasswordResetDoneView(PasswordResetDoneView):
  template_name = 'accounts/reset-done.html'

  def get_context_data(self, *args, **kwargs):
    context = super(UserPasswordResetDoneView, self).get_context_data(*args, **kwargs)
    context['segment'] = 'reset_done_page'
    return context
  

class UserPasswordResetCompleteView(PasswordResetCompleteView):
  template_name = 'accounts/reset-complete.html'

  def get_context_data(self, *args, **kwargs):
    context = super(UserPasswordResetCompleteView, self).get_context_data(*args, **kwargs)
    context['segment'] = 'reset_complete_page'
    return context
  
class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password-change.html'
  form_class = UserPasswordChangeForm

  def get_context_data(self, *args, **kwargs):
    context = super(UserPasswordChangeView, self).get_context_data(*args, **kwargs)
    context['segment'] = 'password_change_page'
    return context

class UserPasswordChangeDoneView(PasswordChangeDoneView):
  template_name = 'accounts/change-done.html'

  def get_context_data(self, *args, **kwargs):
    context = super(UserPasswordChangeDoneView, self).get_context_data(*args, **kwargs)
    context['segment'] = 'change_done_page'
    return context
  
def user_logout(request):
  logout(request)
  return redirect('/accounts/login/')

@login_required(login_url='/accounts/login/')
def lock(request):
  context = {
    'segment': 'lock_page'
  }
  return render(request, 'accounts/lock.html', context)


