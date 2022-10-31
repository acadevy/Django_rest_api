from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from vehicle.models import DateControls,User,Location,attrgetter





user_type = (
    "Dealer",
    "Personal",
    "Organization"
)

# Create your models here.
class UserProfilemodel(models.Model):
    user = models.OneToOneField(User,related_name="user_profile",on_delete=models.CASCADE)
    phone_number = models.PositiveIntegerField()
    user_type = models.CharField(max_length=15,choices=((i,i) for i in user_type))
    location = models.ForeignKey(Location,related_name="users",on_delete=models.CASCADE)

    def save(self,*args,**kwargs):
        # save the location first
        try:
           city,state,country = attrgetter('city',"state","country")(kwargs)
           location = Location.objects.create(city=city, state=state, country=country)
        except Exception as e:
            # log error info E
            location = Location.objects.get(city=city,state=state,country=country)

        self.location = location
        super(UserProfilemodel,self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.user.email}"
