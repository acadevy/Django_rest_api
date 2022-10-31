from django.contrib import admin

from .models import Location,Brand,VehicleModel,Feature,Image,Vehicle

# Register your models here.
admin.site.register((Location,Brand,VehicleModel,Feature,Image,Vehicle))
