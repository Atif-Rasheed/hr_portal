# Generated by Django 4.2.7 on 2023-11-22 11:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('job', '0003_job_employment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplicant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('applicant_id', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('prospect_phone', models.CharField(max_length=255)),
                ('apply_date', models.DateField()),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_jobs', to='job.job')),
            ],
            options={
                'verbose_name': 'Applicant',
                'verbose_name_plural': 'Applicants',
                'db_table': 'applicant_applicants',
            },
        ),
    ]
