from django.db import models
from django.utils import timezone


# Create your models here.
# admin database
class Hmsadmin(models.Model):
    
    name = models.CharField(max_length=100)
    phone = models.IntegerField(unique=True)
    email = models.CharField(unique=True,max_length=100)
    joindate = models.DateField(default=timezone.now)
    enddate = models.TimeField(null=True,blank=True)
    salary = models.IntegerField(null=True, blank=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} (admin)"
    

# admin log in data (date and time)

class Adminlogindata(models.Model):
   
    aid = models.ForeignKey(Hmsadmin,on_delete=models.CASCADE)
    indate = models.DateField(default=timezone.now)
    intime = models.TimeField(default=timezone.now)

    outdate = models.DateField(null=True,blank=True)
    outtime = models.TimeField(null=True,blank=True) 
    
    

# department name and id here
class Department(models.Model):
    
    name = models.CharField(unique=True,max_length=10)

    def __str__(self):
        return self.name
    

# patients database
class Patient(models.Model):
    name = models.CharField(max_length=50)
    disease = models.CharField(max_length=100)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    bedno = models.CharField(max_length=10)
    phone = models.BigIntegerField(null=True,blank=True,unique=False)
    indate = models.DateField(default=timezone.now)
    outdate = models.DateField(null=True,blank=True)
    # remove the admitted by from html files\
    def __str__(self):
        return f"{self.name} (patient)"
    




class Dp(models.Model):
    pid = models.IntegerField(null=False)
    ptype = models.CharField(null=False,max_length=10)
    image = models.ImageField(upload_to="")
    def __str__(self):
        return str(self.pid)+"-"+self.ptype