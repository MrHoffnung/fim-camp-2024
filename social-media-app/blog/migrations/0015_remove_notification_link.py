# Generated by Django 5.0.7 on 2024-08-01 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_remove_notification_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='link',
        ),
    ]
