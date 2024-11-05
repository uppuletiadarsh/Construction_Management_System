# Generated by Django 5.0.7 on 2024-11-05 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application1', '0003_manager_email_manager_mobile_number_manager_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='worker',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='skill',
        ),
        migrations.AddField(
            model_name='task',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='task_images/'),
        ),
        migrations.AddField(
            model_name='task',
            name='workers',
            field=models.ManyToManyField(blank=True, to='Application1.worker'),
        ),
        migrations.AddField(
            model_name='worker',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='worker',
            name='token_no',
            field=models.CharField(default='', max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
