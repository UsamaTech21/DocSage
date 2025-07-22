

# Register your models here.
from django.contrib import admin
from .models import Doctor  # Ensure this model is defined in doctors/models.py

admin.site.register(Doctor)
