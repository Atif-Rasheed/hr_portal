# Generated by Django 4.2.7 on 2023-12-26 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_workflow_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(max_length=100, verbose_name='ID'),
        ),
    ]
