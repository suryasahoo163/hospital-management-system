from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.userdashboard ,name= ""),

    path('/userdashboard',views.userdashboard ,name= "userdashboard"),
    path('/changeUserPassword',views.changeUserPassword ,name= "changeUserPassword"),
    path('/uploadDP',views.uploadDP ,name= "uploadDP"),
    
    path('/userbookappointment',views.userbookappointment ,name= "userbookappointment"), # page
    path('/bookAppointment',views.bookAppointment ,name= "bookAppointment"), # command/ action
    path('/userhistory',views.userhistory ,name= "userhistory"),

    path("/logout",views.logout,name="logout")
    


]



