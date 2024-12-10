import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.

    
class Campus(models.Model):
    campus_name = models.CharField(max_length=10)

    def __str__(self):
        return self.campus_name

class Building_Type(models.Model):
    type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.type_name

class Building(models.Model):
    building_name = models.CharField(max_length=10)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, default='')
    type = models.ForeignKey(Building_Type, on_delete=models.CASCADE, default='', blank=True)

    def __str__(self):
        return self.building_name

class Item_type(models.Model):
    item_type_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.item_type_name

class Item(models.Model):
    found_date = models.DateField("date_found")
    name = models.CharField(max_length=100, default='')
    note = models.CharField(max_length=100, default="")
    status = models.BooleanField(default=False)
    exact_position = models.CharField(max_length=100, default='', blank=True, null=True)
    founder = models.CharField(max_length=100, default='')
    current_position = models.CharField(max_length=100, default='', blank=True,  null=True)
    type = models.ForeignKey(Item_type, on_delete=models.CASCADE, default='')


    campus_found = models.ForeignKey(Campus, on_delete=models.CASCADE, default='')
    building_found = models.ForeignKey(Building, on_delete=models.CASCADE, default='')

    owner = models.CharField(max_length=100, default='', blank=True,  null=True)
    image = models.ImageField(upload_to="images", default="img1.jpg")

    def __str__(self):
        return self.type.item_type_name + " " + self.note
    
    def published_recently(self):
        return self.found_date >= timezone.now() - datetime.timedelta(days=1)
    