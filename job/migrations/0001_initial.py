# Generated by Django 4.2.7 on 2023-12-15 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField(null=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('workflow_id', models.CharField(max_length=150)),
                ('job_id', models.CharField(max_length=150, null=True, unique=True)),
                ('job_status', models.CharField(choices=[('1', 'Open (default)'), ('3', 'On Hold'), ('8', 'Approved'), ('7', 'Needs Approval'), ('2', 'Drafting'), ('4', 'Filled'), ('5', 'Canceled'), ('6', 'Closed')], default=1, max_length=10)),
                ('employment_type', models.CharField(choices=[('1', 'Full Time'), ('2', 'Part Time'), ('3', 'Part Time to Full Time'), ('4', 'Temporary'), ('5', 'Temporary to Full Time'), ('6', 'Contracted'), ('7', 'Contracted to Full Time'), ('8', 'Internship'), ('9', 'Internship to Full Time'), ('10', 'Volunteer'), ('11', 'Seasonal')], default=1, max_length=10)),
                ('minimum_experience', models.CharField(choices=[('1', 'Student (High School)'), ('2', 'Student (College)'), ('3', 'Entry Level'), ('4', 'Mid Level'), ('5', 'Experienced'), ('6', 'Manager/Supervisor'), ('7', 'Senior Manager/Supervisor'), ('8', 'Executive'), ('9', 'Senior Executive')], default=1, max_length=10)),
                ('confidential', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=255)),
                ('private', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=255)),
                ('canned_address', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Address', max_length=10)),
                ('canned_cover_letter', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Cover Letter', max_length=10)),
                ('canned_references', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='References', max_length=10)),
                ('canned_wmyu', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='What Makes You Unique', max_length=10)),
                ('canned_linked_in', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='LinkedIn', max_length=10)),
                ('canned_website', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Website, blog or portfolio', max_length=10)),
                ('canned_twitter_username', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Twitter Username', max_length=10)),
                ('canned_start', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Earliest Start Date', max_length=10)),
                ('canned_weekends', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Work Weekends', max_length=10)),
                ('canned_evenings', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Work Evenings', max_length=10)),
                ('canned_overtime', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Work Overtime', max_length=10)),
                ('canned_languages', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Language Spoken', max_length=10)),
                ('canned_salary', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Desired Salary', max_length=10)),
                ('canned_referral', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Referral Name', max_length=10)),
                ('canned_license', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Valid Drivers License', max_length=10)),
                ('canned_cdl', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Commercial Driving License', max_length=10)),
                ('canned_relocate', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Willing to Relocate', max_length=10)),
                ('canned_citizen', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Citizen/Employment Status', max_length=10)),
                ('canned_education', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Highest Education Obtained', max_length=10)),
                ('canned_college', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='College/University', max_length=10)),
                ('canned_gpa', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Grade Point Average(GPA)', max_length=10)),
                ('canned_over18', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Age 18 or Older', max_length=10)),
                ('canned_flighthours', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Pilot - Flight Hours', max_length=10)),
                ('canned_flightgrade', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Pilot - Grade/Ratings', max_length=10)),
                ('canned_felony', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Felony Conviction', max_length=10)),
                ('canned_felonyexplain', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Felony Explanation', max_length=10)),
                ('approved_salary_range_minimum', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Minimum salary')),
                ('approved_salary_range_maximum', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Maximum Salary')),
                ('department', models.CharField(blank=True, max_length=300, null=True, verbose_name='Department')),
                ('state', models.CharField(blank=True, max_length=255, null=True, verbose_name='State')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='City')),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Postal Code')),
                ('internal_job_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Internal Job Code')),
                ('eeo_1_job_category', models.CharField(blank=True, choices=[('1', 'Executive/Senior Level Officials and Managers'), ('2', 'Professionals'), ('3', 'Technicians'), ('4', 'Sales Workers'), ('5', 'Administrative Support Workers'), ('6', 'Craft Workers'), ('7', 'Operatives'), ('8', 'Laborers and Helpers'), ('9', 'Service Workers'), ('10', 'First/Mid Level Officials & Managers')], max_length=255, null=True, verbose_name='Job Category')),
                ('syndication', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', help_text='Indicates whether the job is syndicated to Indeed, Simply Hired, and other job boards.', max_length=255)),
                ('open_date', models.DateField(blank=True, help_text='The Date that the Job was originally created. Use YYYY-MM-DD format', null=True, verbose_name='Open Date')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_%(app_label)s_%(class)s', to=settings.AUTH_USER_MODEL)),
                ('hiring_lead', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Job',
                'verbose_name_plural': 'Jobs',
                'db_table': 'job_jobs',
            },
        ),
        migrations.CreateModel(
            name='JobTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField(null=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('workflow_id', models.CharField(max_length=150)),
                ('job_id', models.CharField(max_length=150, null=True, unique=True)),
                ('job_status', models.CharField(choices=[('1', 'Open (default)'), ('3', 'On Hold'), ('8', 'Approved'), ('7', 'Needs Approval'), ('2', 'Drafting'), ('4', 'Filled'), ('5', 'Canceled'), ('6', 'Closed')], default=1, max_length=10)),
                ('employment_type', models.CharField(choices=[('1', 'Full Time'), ('2', 'Part Time'), ('3', 'Part Time to Full Time'), ('4', 'Temporary'), ('5', 'Temporary to Full Time'), ('6', 'Contracted'), ('7', 'Contracted to Full Time'), ('8', 'Internship'), ('9', 'Internship to Full Time'), ('10', 'Volunteer'), ('11', 'Seasonal')], default=1, max_length=10)),
                ('minimum_experience', models.CharField(choices=[('1', 'Student (High School)'), ('2', 'Student (College)'), ('3', 'Entry Level'), ('4', 'Mid Level'), ('5', 'Experienced'), ('6', 'Manager/Supervisor'), ('7', 'Senior Manager/Supervisor'), ('8', 'Executive'), ('9', 'Senior Executive')], default=1, max_length=10)),
                ('confidential', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=255)),
                ('private', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=255)),
                ('canned_address', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Address', max_length=10)),
                ('canned_cover_letter', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Cover Letter', max_length=10)),
                ('canned_references', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='References', max_length=10)),
                ('canned_wmyu', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='What Makes You Unique', max_length=10)),
                ('canned_linked_in', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='LinkedIn', max_length=10)),
                ('canned_website', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Website, blog or portfolio', max_length=10)),
                ('canned_twitter_username', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Twitter Username', max_length=10)),
                ('canned_start', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Earliest Start Date', max_length=10)),
                ('canned_weekends', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Work Weekends', max_length=10)),
                ('canned_evenings', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Work Evenings', max_length=10)),
                ('canned_overtime', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Work Overtime', max_length=10)),
                ('canned_languages', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Language Spoken', max_length=10)),
                ('canned_salary', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Desired Salary', max_length=10)),
                ('canned_referral', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Referral Name', max_length=10)),
                ('canned_license', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Valid Drivers License', max_length=10)),
                ('canned_cdl', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Commercial Driving License', max_length=10)),
                ('canned_relocate', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Willing to Relocate', max_length=10)),
                ('canned_citizen', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Citizen/Employment Status', max_length=10)),
                ('canned_education', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Highest Education Obtained', max_length=10)),
                ('canned_college', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='College/University', max_length=10)),
                ('canned_gpa', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Grade Point Average(GPA)', max_length=10)),
                ('canned_over18', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Age 18 or Older', max_length=10)),
                ('canned_flighthours', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Pilot - Flight Hours', max_length=10)),
                ('canned_flightgrade', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Pilot - Grade/Ratings', max_length=10)),
                ('canned_felony', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Felony Conviction', max_length=10)),
                ('canned_felonyexplain', models.CharField(choices=[('0', 'Not Selected, Not Required'), ('1', 'Selected, Not Required'), ('3', 'Selected, Required')], default=0, help_text='Felony Explanation', max_length=10)),
                ('approved_salary_range_minimum', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Minimum salary')),
                ('approved_salary_range_maximum', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Maximum Salary')),
                ('department', models.CharField(blank=True, max_length=300, null=True, verbose_name='Department')),
                ('state', models.CharField(blank=True, max_length=255, null=True, verbose_name='State')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='City')),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Postal Code')),
                ('internal_job_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Internal Job Code')),
                ('eeo_1_job_category', models.CharField(blank=True, choices=[('1', 'Executive/Senior Level Officials and Managers'), ('2', 'Professionals'), ('3', 'Technicians'), ('4', 'Sales Workers'), ('5', 'Administrative Support Workers'), ('6', 'Craft Workers'), ('7', 'Operatives'), ('8', 'Laborers and Helpers'), ('9', 'Service Workers'), ('10', 'First/Mid Level Officials & Managers')], max_length=255, null=True, verbose_name='Job Category')),
                ('syndication', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', help_text='Indicates whether the job is syndicated to Indeed, Simply Hired, and other job boards.', max_length=255)),
                ('open_date', models.DateField(blank=True, help_text='The Date that the Job was originally created. Use YYYY-MM-DD format', null=True, verbose_name='Open Date')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by_job_templates', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_by_job_templates', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Job Template',
                'verbose_name_plural': 'Job Templates',
                'db_table': 'job_job_templates',
            },
        ),
        migrations.CreateModel(
            name='TestlifyLink',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField(null=True)),
                ('link', models.URLField(verbose_name='Job Link')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_testlify_link', to=settings.AUTH_USER_MODEL)),
                ('job_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testlify_links', to='job.jobtemplate')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_by_testlify_link', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Testlify Link',
                'verbose_name_plural': 'Testlify Links',
                'db_table': 'job_testlify_link',
            },
        ),
        migrations.CreateModel(
            name='KnockoutCriteria',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField(null=True)),
                ('minimum_experience', models.CharField(choices=[('experience1', 'Experience 1'), ('experience2', 'Experience 2')], max_length=50)),
                ('job_description_option', models.CharField(choices=[('template', 'Template'), ('manual', 'Manual')], max_length=50)),
                ('manual_job_description', models.TextField(blank=True)),
                ('education_level', models.CharField(blank=True, max_length=50)),
                ('multiple_languages', models.BooleanField(default=False)),
                ('no_college', models.BooleanField(default=False)),
                ('felon', models.BooleanField(default=False)),
                ('no_references', models.BooleanField(default=False)),
                ('not_citizen', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by_criteria_knockout', to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_criteria_knockout', to='job.job')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_by_criteria_knockout', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='job_template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job.jobtemplate'),
        ),
        migrations.AddField(
            model_name='job',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_%(app_label)s_%(class)s', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField(null=True)),
                ('ease_of_use', models.CharField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')], max_length=10)),
                ('features', models.CharField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')], max_length=10)),
                ('comments', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by_feedback', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_by_feedback', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
            ],
            options={
                'verbose_name': 'Dashboard',
                'verbose_name_plural': 'Dashboard',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('job.job',),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('job.job',),
        ),
    ]
