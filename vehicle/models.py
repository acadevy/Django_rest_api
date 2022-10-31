from distutils.command.upload import upload
from enum import unique
from tkinter import E
from django.db import models
from django.contrib.auth.models import User
from operator import attrgetter
# Create your models here.


vehicle_types = (
    "Sedan",
    "Coupe",
    "Sport car",
    "Station wagon",
    "Convertible",
    "SAN",
    "Minivan",
    "Pickup"
)

gear_types = (
    "Manual",
    "Automatic"
)

vehicle_conditions = (
    "brand new",
    "Locally used"
)


class DateControls(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Location(DateControls):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)


    class Meta:
        unique_together = ("city","state","country")

    def __str__(self):
        return f"{self.city} - {self.state} - {self.country}"





class Brand(DateControls):
    name = models.CharField(max_length=100,unique=True)


    def __str__(self):
        return self.name



class VehicleModels(DateControls):
    brand = models.ForeignKey(Brand,related_name="vehicles",on_delete=models.CASCADE)
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

    



class VehicleModel(DateControls):
    brand = models.ForeignKey(Brand,related_name="models",on_delete=models.CASCADE)
    name = models.CharField(max_length=100,unique=True)

    class Meta:
        unique_together = ("brand","name")

class Feature(DateControls):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Vehicle(DateControls):
    added_by = models.ForeignKey(User,related_name="user_vehicles",on_delete=models.CASCADE)
    model = models.ForeignKey(User,related_name="vehicles",on_delete=models.CASCADE)
    common_name = models.CharField(max_length=150)
    vehicle_type = models.CharField(max_length=20,choices=((i,i) for i in vehicle_types))
    gear_type = models.CharField(max_length=15,choices=((i,i) for i in gear_types))
    condition = models.CharField(max_length=15,choices=((i,i) for i in vehicle_conditions))
    year = models.PositiveIntegerField()
    location = models.ForeignKey(Location,related_name="vehicles", on_delete=models.CASCADE)
    mileage = models.FloatField()
    float = models.FloatField()
    negotiable = models.BooleanField()
    features = models.ManyToManyField(Feature,related_name="vehicle_features")

    def save(self,*args,**kwargs):
        # save the location first
        try:
           city,state,country = attrgetter('city',"state","country")(kwargs)
           location = Location.objects.create(city=city, state=state, country=country)
        except Exception as e:
            # log error info E
            location = Location.objects.get(city=city,state=state,country=country)

        self.location = location
        super(VehicleModel,self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.common_name} - {self.created_at}"
       

class Image(DateControls):
    vehicle = models.ForeignKey(Vehicle, related_name="images",on_delete=models.CASCADE)
    image = models.ImageField(upload_to="cars_images")

    def __str__(self):
        return f"{self.vehicle.common_name} - {self.created_at}"

