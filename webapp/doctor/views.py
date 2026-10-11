from django.shortcuts import render,redirect
from hmsadmin.models import Patient, Department
from user.models import Appointment
from django.db.models import  F
from django.http import JsonResponse
from django.utils import timezone
from .models import Doctor,Doctorlogindata
from hmsadmin.models import Dp

# Create your views here.
def doctordashboard(request):
    # login doctor data validation
    if request.session["did"]:
        id = request.session.get("did")
        PnAdata = {"patients":Patient.objects.filter(department = Doctor.objects.get(id = id).department.id,outdate__isnull=True).count(),"ap":Appointment.objects.filter(cdate__isnull = True).count()}
        return render(request,'doctordashboard.html',context={"dashData":PnAdata})

def doctorappointments(request):
    appointments = Appointment.objects.filter(cdate__isnull = True).order_by("date","-id")
    return render(request,'doctorappointments.html',context={'appointments':appointments})

def closeAppointment(request,id):
    delete = Appointment.objects.get(id = id)
    delete.cdate = timezone.now()
    delete.save()
    return redirect(doctorappointments)
# render all patients
def doctorpatients(request):
    department = Doctor.objects.get(id = int(request.session["did"])).department
    
    patientsData = Patient.objects.filter(department = department).order_by(F('outdate').desc(nulls_first=True),"-outdate","-id")

    return render(request,'doctorpatients.html',context={'department':department,"patients":patientsData})
# render active patients to search
def doctorsearch(request):
    availablePatients = Patient.objects.filter(outdate = None ).order_by("-indate","-id")
    return render(request,'doctorsearch.html',context={'patients':availablePatients})


def searchPatient(request):
    if request.method == "GET":
        column = request.GET["column"]
        value = request.GET["filterElement"]
        column = str(column).lower()
        value = str(value).lower()
        patientSearchData = []
        for data in Patient.objects.all():
            valueFromSet = getattr(data,column)
            try:
                if valueFromSet == int(value):
                    patientSearchData.append(data.id)
                
            except:
                if str(valueFromSet).lower() == value:
                    patientSearchData.append(data.id)
            finally:
                pass

        filteredPatients = Patient.objects.filter(id__in = patientSearchData)
        patientSearchData =[]
        for patient in filteredPatients:
            patientSearchData.append(
        {
            'id' : str(patient.id),
            'name' : patient.name,
            'disease': patient.disease,
            'department' : str(patient.department),
            'phone' : str(patient.phone),
            'bedno':patient.bedno,
            'indate' :  str(patient.indate),
            'outdate': str(patient.outdate)
        })
        return JsonResponse({'data':patientSearchData})
   



def addPatient(request):
    if request.method == "POST":
        name = request.POST['name']
        name = str(name).title()
        bedno = str(request.POST['bedno']).capitalize()
        phone = int(request.POST['phone'])
        disease = request.POST['disease']
        disease = str(disease).capitalize()
        department = request.POST['department']
        department = Department.objects.get(id = int(department))

        patient = Patient.objects.create(name = name,bedno = bedno,phone=phone,disease=disease,department=department)
        patient.save()
    return redirect(doctorpatients)



def dischargePatient(request,id):
    patient = Patient.objects.get(id = id)
    patient.outdate = timezone.now()
    patient.save()

    return redirect(doctorpatients)

def doctorlogout(request):
    doctorSessionData = Doctorlogindata.objects.get(did = request.session["did"], outtime__isnull = True)
    doctorSessionData.outdate = timezone.now()
    doctorSessionData.outtime = timezone.now()
    doctorSessionData.save()
    del request.session['did']
    request.session.modified = True 
    return redirect("doctorlogin")


def doctorDp(request):
    if request.method == "POST":
        pid = request.session.get("did")
        ptype = "doctor"
        image= request.FILES.get("dp")

        try:
            dp = Dp.objects.get(pid=int(pid),ptype=ptype)
            dp.image = image
            dp.save()
        except:
            Dp.objects.create(pid = int(pid),ptype=ptype,image=image)

    return redirect(doctordashboard)