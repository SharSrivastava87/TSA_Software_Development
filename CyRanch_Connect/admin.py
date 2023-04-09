from django.contrib import admin
from .models import *

# Registered models
admin.site.register(Event)
admin.site.register(Student)
admin.site.register(Prize)