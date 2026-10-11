from django.contrib import admin
from django.urls import path, include
from hmsadmin import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',views.admindashboard,name=''),

    path('/admindashboard',views.admindashboard,name='admindashboard'),
    path('/adminDp',views.adminDp,name='adminDp'),
    
    path('/admindoctors',views.admindoctors,name='admindoctors'),
    path('/admindoctorsessionlogs',views.admindoctorsessionlogs,name='admindoctorsessionlogs'),
    path('/addDoctor',views.addDoctor,name='addDoctor'),
    path('/validateEF',views.validateEF,name='validateEF'),
    path('/validateEFforID',views.validateEFforID,name='validateEFforID'),
    
    path('/deleteDoctor/<int:id>', views.deleteDoctor, name='deleteDoctor'),

    
    path('/fetchDoctorData', views.fetchDoctorData, name='fetchDoctorData'),
    path('/editDoctor/', views.editDoctor, name='editDoctor'),

    path('/adminqueries',views.adminqueries,name = "adminqueries"),
    path('/send_response/<int:id>',views.send_response,name = "send_response"),

    path('/adminpatients',views.adminpatients,name='adminpatients'),
    path('/adminpatientshistory',views.adminpatientshistory,name='adminpatientshistory'),


    path('/adminpatientssearch',views.adminpatientssearch,name='adminpatientssearch'),
    path('/searchPatient',views.searchPatient,name='searchPatient'),


    path('/adminqueries',views.adminqueries,name='adminqueries'),
    path('/adminusers',views.adminusers,name='adminusers'),
    path('/adminusersessionlogs',views.adminusersessionlogs,name='adminusersessionlogs'),

    path('/adminlogout',views.adminlogout,name='adminlogout'),
]

