from django.db import models

from django.utils import timezone

# Create your models here.
# Doctor database

class Doctor(models.Model):
  
    name = models.CharField(max_length=100,)
    phone = models.IntegerField(unique=True)
    email = models.CharField(unique=True,max_length=100)
    joindate = models.DateField(default=timezone.now)
    enddate = models.CharField(default="Active",max_length=15)
    salary = models.IntegerField(null=True, blank=True)
    department = models.ForeignKey("hmsadmin.Department",on_delete=models.CASCADE)
    password = models.CharField(max_length=100,)


    def __str__(self):
        return f"{self.name} ({self.department})"


# doctor login data
class Doctorlogindata(models.Model):
    
    did = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    indate = models.DateField(default=timezone.now)
    intime = models.TimeField(default=timezone.now)

    outdate = models.DateField(null=True,blank=True)
    outtime = models.TimeField(null=True,blank=True) 
    
    
