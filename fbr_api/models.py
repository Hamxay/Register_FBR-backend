from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
# Create your models here.

class RegisterUser(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    cnic = models.CharField(max_length=13 , unique=True , blank=True)

class FBR(models.Model):
    user = models.ForeignKey(RegisterUser , on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100,blank=True)
    district = models.CharField(max_length=100,blank=True)
    police_station = models.CharField(max_length=100,blank=True)
    catagory = models.CharField(max_length=100,blank=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    mobile_number = models.IntegerField(null=True,blank=True)
    description = models.TextField()
    is_seen = models.BooleanField(default=False)