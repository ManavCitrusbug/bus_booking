
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField
from datetime import datetime,time
    

class Category(models.Model):
    category=models.CharField(max_length=50)
    def __str__(self):
        return self.category


class Transport(models.Model):
    transport_name=models.CharField(max_length=100)
    number_plate=models.CharField(max_length=20)
    seats_available=models.IntegerField()
    price_per_person=models.IntegerField()
    bus_category=models.ForeignKey(Category,on_delete=models.CASCADE)
    available=models.BooleanField(default=True)
    date_time_dpt=models.DateField()
    def __str__(self):
        return self.transport_name


class Booked_bus(models.Model):
    busname=models.ForeignKey(Transport,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=15)
    age=models.IntegerField()
    book_date_time=models.DateField()
    paid=models.BooleanField(default=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)



class Journey(models.Model):
    start_point=models.CharField(max_length=20)
    end_point=models.CharField(max_length=20)
    transport=models.ManyToManyField(Transport)


    def Buses(self):
        return ".".join([str(b) for b in self.transport.all() ])



