# Generated by Django 4.1.5 on 2023-03-17 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CyRanch_Connect', '0014_remove_student_events_event_attendees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(blank=True, to='CyRanch_Connect.student'),
        ),
    ]
