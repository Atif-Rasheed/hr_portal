# Generated by Django 4.2.7 on 2023-12-15 19:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='job',
            unique_together={('hiring_lead', 'job_template')},
        ),
    ]
