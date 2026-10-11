from django.db import models
from hmsadmin.models import Department
from django.utils import timezone
# Create your models here.

# create user database
class User(models.Model):
   
    name = models.CharField(max_length=100)
    phone = models.IntegerField(unique=True)
    email = models.CharField(unique=True,max_length=100)
    joindate = models.DateField(default=timezone.now)
    password = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.name} (user)"

# user login data
class Userlogindata(models.Model):
    
    uid = models.ForeignKey(User,on_delete=models.CASCADE)
    indate = models.DateField(default=timezone.now)
    intime = models.TimeField(default=timezone.now)

    outdate = models.DateField(null=True,blank=True)
    outtime = models.TimeField(null=True,blank=True)
    def save(self,*arg,**kwarg):
        if self.uid:
            self.name = self.uid.name
        super().save(*arg,**kwarg)

# user query database
class Query(models.Model):
  
    name = models.CharField(max_length=50)
    phone = models.IntegerField(null=False,blank=False)
    email = models.CharField(max_length=100)
    age = models.IntegerField(null=False,blank=False)
    gender = models.CharField(max_length=6)
    address = models.CharField(max_length=100)
    query = models.CharField(max_length= 500)
    date = models.DateField(default=timezone.now)
    response = models.CharField(max_length=500,default='',blank=True)

    def __str__(self):
        return f"{self.name} : {self.query}"

# user appintment databse
class Appointment(models.Model):
   
    uid = models.ForeignKey(User,on_delete=models.RESTRICT)
    name = models.CharField(max_length=50)
    phone = models.IntegerField(null=False,blank = True)
    reason = models.CharField(max_length=500)
    date = models.DateField(default=timezone.now)
    cdate = models.DateField(null=True,blank=True)
    
    def __str__(self):
        return f'{self.name} : {self.reason}'



