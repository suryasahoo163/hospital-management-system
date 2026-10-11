"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home ,name= "home"),
    
    path("userlogin",views.userlogin,name='userlogin'),
    path("userregistration",views.userregistration,name='userregistration'), # renders the page
 
    path("userRegistration",views.userRegistration,name='userRegistration'), # perform action of the page
    path("doctorlogin",views.doctorlogin,name='doctorlogin'),
    path("validateEP",views.validateEP,name='validateEP'),
    path("adminlogin",views.adminlogin,name='adminlogin'),
    path("userquery",views.userquery,name='userquery'),

    path("userAuth",views.userAuth,name="userAuth"), # user authentication
    path("doctorAuth",views.doctorAuth,name="doctorAuth"), # user authentication
    path("adminAuth",views.adminAuth,name="adminAuth"), # admin authentication

    
]
