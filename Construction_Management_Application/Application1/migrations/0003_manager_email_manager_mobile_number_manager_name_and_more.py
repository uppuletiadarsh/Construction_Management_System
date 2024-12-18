# Generated by Django 5.0.7 on 2024-10-24 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application1', '0002_worker_supervisor_project_supervisor_task_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='email',
            field=models.EmailField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manager',
            name='mobile_number',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manager',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supervisor',
            name='email',
            field=models.EmailField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supervisor',
            name='mobile_number',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supervisor',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
