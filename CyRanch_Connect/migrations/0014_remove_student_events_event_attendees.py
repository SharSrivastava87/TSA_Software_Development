# Generated by Django 4.1.5 on 2023-03-17 04:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CyRanch_Connect', '0013_alter_event_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='events',
        ),
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
