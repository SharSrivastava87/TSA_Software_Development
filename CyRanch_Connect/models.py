from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Student model is connected to a user model which is to be used for authentication
class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='student')
    grade = models.IntegerField(null=True, validators=[MinValueValidator(9), MaxValueValidator(12)])
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    student_id = models.IntegerField(null=True)
    email = models.EmailField(max_length=200)
    points = models.IntegerField(blank=True, default=0)

    # Modify metadata for proper representation of the model when it is displayed in the admin panel
    def __str__(self):
        return self.first_name + ' ' + self.last_name

    # Modify the default ordering for the student models in order to quickly find the student with the most points
    class Meta:
        get_latest_by = 'points'


# An event object that stores information about an event, events can be added through the admin panel
class Event(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    # The date and time are used in order to only display events that have not happened yet
    date = models.DateTimeField()
    points = models.IntegerField(null=False, default=1)
    location = models.CharField(max_length=200, null=True)
    latitude = models.FloatField(default=0, null=False)
    longitude = models.FloatField(default=0, null=False)
    event_id = models.SlugField(blank=False, null=True)
    # A secret token used to generate ephemeral QR codes for each event
    token = models.IntegerField(default=0, editable=False)
    attendees = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return self.name


# A prize object, prizes can be added through the admin panel
class Prize(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=False, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', null=True)

    def __str__(self):
        return self.name
