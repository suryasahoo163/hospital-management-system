from django.contrib import admin
from django.urls import path, include
# from website import views
from . import views

from django.conf import settings
from django.conf.urls.static import static
#######


urlpatterns = [
    path('',views.doctordashboard,name=''),
    path('/doctordashboard',views.doctordashboard,name='doctordashboard'),
    path('/doctorDp',views.doctorDp,name='doctorDp'),

    path('/doctorappointments',views.doctorappointments,name='doctorappointments'),
    path('/closeAppointment/<int:id>',views.closeAppointment,name='closeAppointment'),

    path('/doctorpatients',views.doctorpatients,name='doctorpatients'),

    
    path('/doctorsearch',views.doctorsearch,name='doctorsearch'),
    path('/searchPatient',views.searchPatient,name='searchPatient'),

    path('/addPatient',views.addPatient,name='addPatient'),
    path('/dischargePatient/<int:id>',views.dischargePatient,name='dischargePatient'),
    path('/doctorlogout',views.doctorlogout,name='doctorlogout'),

]
