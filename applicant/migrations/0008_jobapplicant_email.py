# Generated by Django 4.2.7 on 2024-01-18 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0007_rename_jobapplicantappliedjobs_jobapplicantappliedjob'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplicant',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='Email'),
        ),
    ]
