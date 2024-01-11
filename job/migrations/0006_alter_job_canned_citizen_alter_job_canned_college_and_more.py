# Generated by Django 4.2.7 on 2024-01-11 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0005_alter_job_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='canned_citizen',
            field=models.BooleanField(default=False, help_text='Citizen/Employment Status'),
        ),
        migrations.AlterField(
            model_name='job',
            name='canned_college',
            field=models.BooleanField(default=False, help_text='College/University'),
        ),
        migrations.AlterField(
            model_name='job',
            name='canned_education',
            field=models.BooleanField(default=False, help_text='Highest Education Obtained'),
        ),
        migrations.AlterField(
            model_name='job',
            name='canned_felony',
            field=models.BooleanField(default=False, help_text='Felony Conviction'),
        ),
        migrations.AlterField(
            model_name='job',
            name='canned_languages',
            field=models.BooleanField(default=False, help_text='Language Spoken'),
        ),
        migrations.AlterField(
            model_name='job',
            name='canned_over18',
            field=models.BooleanField(default=False, help_text='Age 18 or Older'),
        ),
    ]
