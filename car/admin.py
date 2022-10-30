from msilib.schema import Feature
from django.contrib import admin
from .models import Manufacturer,Car,Feature

# Register your models here.
admin.site.register((Car,Manufacturer,Feature))

