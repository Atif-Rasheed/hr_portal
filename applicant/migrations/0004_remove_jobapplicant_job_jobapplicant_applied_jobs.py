# Generated by Django 4.2.7 on 2024-01-18 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_alter_job_canned_citizen_alter_job_canned_college_and_more'),
        ('applicant', '0003_jobapplicant_email_alter_jobapplicant_rating_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobapplicant',
            name='job',
        ),
        migrations.AddField(
            model_name='jobapplicant',
            name='applied_jobs',
            field=models.ManyToManyField(blank=True, related_name='applicants', to='job.job'),
        ),
    ]
