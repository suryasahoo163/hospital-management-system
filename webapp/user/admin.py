from django.contrib import admin
from .models import *
from .models import User
# Register your models here.


admin.site.register(User)
admin.site.register(Userlogindata)
admin.site.register(Query)
admin.site.register(Appointment)