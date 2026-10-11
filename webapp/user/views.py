from django.shortcuts import render,redirect
from .models import User, Appointment,Userlogindata
from django.utils import timezone
from django.db.models import F
from django.http import JsonResponse
from hmsadmin.models import Dp
# Create your views here.

# render user dashboard
def userdashboard(request):
    if request.session['uid']:
    # authentication
        id = request.session.get("uid")
       
        n_appointments = {"completed":Appointment.objects.filter(uid = id, cdate__isnull = False).count() , "pending": Appointment.objects.filter(uid = id, cdate__isnull = True).count()}

        return render (request,'userdashboard.html',context={"ap":n_appointments})

# render user bookappointment
def userbookappointment(request):
    return render (request,'userbookappointment.html')

def bookAppointment(request):
    if request.method == "POST":
        id = int(str(request.session["uid"]).strip(" "))
        reason = str(request.POST["reason"]).capitalize()
        appointmentDate = request.POST["date"]

        if request.POST["phone"] == request.POST["name"] == "":
            name = User.objects.get(id = id).name
            phone = User.objects.get(id = id).phone
        else:
            name = request.POST["name"]
            phone = request.POST["phone"]
        Appointment.objects.create(uid = User.objects.get(id = id),name=str(name).title(),phone = phone, reason=reason,date = appointmentDate)
        return redirect(userhistory)
    
    return redirect(userbookappointment)
    
# render user history
def userhistory(request):
    id = request.session.get("uid")
    appointments = Appointment.objects.filter(uid = id).order_by(F("cdate").asc(nulls_first=True),"date","-id")
    return render (request,'userhistory.html',context={'appointments':appointments})

def logout(request):
    userSessionData = Userlogindata.objects.get(uid = request.session["uid"], outtime__isnull = True)
    userSessionData.outdate = timezone.now()
    userSessionData.outtime = timezone.now()
    userSessionData.save()
    del request.session['uid']
    request.session.modified = True 
    return redirect("userlogin")

def changeUserPassword(request):
    if request.method == "GET":
        id = request.session["uid"]
        user = User.objects.get(id = id)
        if user.password == str(request.GET["oldpass"]):
            user.password = str(request.GET["newpass"])
            user.save()
            return JsonResponse({"message":"done"})
        else:
            return JsonResponse({"message":"incorrect"})
    return JsonResponse({"message":"error"})

def uploadDP(request):
    if request.method == "POST":
        pid = request.session.get("uid")
        ptype = "user"
        image= request.FILES.get("dp")

        try:
            dp = Dp.objects.get(pid=int(pid),ptype=ptype)
            dp.image = image
            dp.save()
        except:
            Dp.objects.create(pid = int(pid),ptype=ptype,image=image)

    return redirect(userdashboard)