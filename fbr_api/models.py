from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
# Create your models here.

class RegisterUser(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    cnic = models.CharField(max_length=13 , unique=True)

class FBR(models.Model):
    user = models.ForeignKey(RegisterUser , on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    

