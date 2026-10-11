from django.shortcuts import render,redirect
from .models import Department, Patient, Hmsadmin, Adminlogindata, Dp
from doctor.models import Doctor,Doctorlogindata
from user.models import Query, User, Userlogindata, Appointment
import re
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.db.models import F
# Create your views here.

# render dashboard
def admindashboard(request):
    data = {"users":f"{Userlogindata.objects.filter(outdate__isnull = True).count()}/{User.objects.all().count()}",
            "patients":f"{Patient.objects.filter(outdate__isnull=True).count()}",
            "doctors":f"{Doctorlogindata.objects.filter(outdate__isnull = True).count()}/{Doctor.objects.all().count()}",
            "queries":f'{Query.objects.filter(response="").count()}',
            "app":f'{Appointment.objects.filter(cdate__isnull = True).count()}',
            }
    adminData = Hmsadmin.objects.get(id = int(request.session["aid"]))
    return render(request,'admindashboard.html',context={"data":data})

# render doctors
def admindoctors(request):
    doctorData = {'departments' : Department.objects.all(), 'allDoctors':Doctor.objects.all()}

    return render(request,'admindoctors.html',context=doctorData)

# add doctor to data base 
def addDoctor(request):
   
    if request.method == "POST":
        name = str(request.POST.get("name")).title()
        department_id = request.POST.get("department")
    
        department = Department.objects.get(id=department_id) # retrieving department instance using the department id
        
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        salary = request.POST.get("salary")
        password = name.strip().split(" ")[0].title()
       
        Doctor.objects.create(name=name,department=department,email=email,phone=phone,salary=salary,password = password)

    return redirect('admindoctors')

def validateEF(request):
    phoneRE = re.compile(r'^[6-9]\d{9}$')
    emailRE = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    if request.method == "GET":
        phone = request.GET["phone"]
        email = request.GET["email"]

        if phoneRE.match(str(phone)):
            pass
        else:
            return JsonResponse({"message":"Enter a valid phone number"})
        if emailRE.match(email):
            pass
        else:
            return JsonResponse({"message":"Enter a valid email address"})
        
        if phone and email:
            phones = Doctor.objects.values_list("phone",flat=True)
            phones = list(map(str,phones))
            emails = Doctor.objects.values_list("email",flat=True)
            emails = list(map(str,emails))
            if str(email) in emails:
                return JsonResponse({'message': "Email is already exists"})
            elif str(phone) in  phones:
                return JsonResponse({'message':"Phone is already exists"})
            else:
                return JsonResponse({'message':"allow"})
        else:
            return JsonResponse({'message' : 'phone number or email cannot be empty'})
        

def validateEFforID(request):
    phoneRE = re.compile(r'^[6-9]\d{9}$')
    emailRE = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    if request.method == "GET":
        id = int(request.GET["id"])
        phone = int(request.GET["phone"])
        email = request.GET["email"]

        if phoneRE.match(str(phone)):
            pass
        else:
            return JsonResponse({"message":"Enter a valid phone number"})
        if emailRE.match(email):
            pass
        else:
            return JsonResponse({"message":"Enter a valid email address"})
        if phone and email:
            try:
                doctorPhoneData = Doctor.objects.get(phone = phone)
                if doctorPhoneData.id != id:
                    return JsonResponse({'message': "Phone is already exists"})
            except:
                pass
            
            
            try:
                doctorEmailData = Doctor.objects.get(email = email)
                if doctorEmailData.id != id:
                    return JsonResponse({'message': "Email is already exists"})
                else:
                    return JsonResponse({"message":"allow"})
            except:
                return JsonResponse({"message":"allow"})
        else:
            return JsonResponse({'message' : 'phone number or email cannot be empty'})


# delete doctor from the database

def deleteDoctor(request,id):
    if Doctor.objects.get(id=id):
        removeDoctor = Doctor.objects.get(id=id)
        removeDoctor.delete()
    
    return redirect('admindoctors')

# fetch doctor data to the frontend
def fetchDoctorData(request):
    if request.method == "GET":
        id = int(request.GET['id'])
        retrievedData = Doctor.objects.get(id = id)
        doctorData = {
            'id' : retrievedData.id,
            'name' : retrievedData.name,
            'phone' : retrievedData.phone,
            'email' : retrievedData.email,
            'salary' : retrievedData.salary,
            'department': retrievedData.department.id,
        }
        return JsonResponse({'doctor':doctorData})
    
# edit doctor details
def editDoctor(request):
   
    if request.method == "POST":
        id = int(request.POST["id"])
        doctorData = Doctor.objects.get(id = id)
        doctorData.name = str(request.POST["name"]).title()
        doctorData.phone = int(request.POST["phone"])
        doctorData.email = request.POST["email"]
        doctorData.salary = int(request.POST["salary"])
        doctorData.department = Department.objects.get(id = int(request.POST["department"]))
        doctorData.save()
    return redirect('admindoctors')




# render doctorsessionlogs
def admindoctorsessionlogs(request):
    doctors = Doctorlogindata.objects.all().order_by(F("outdate").desc(nulls_first = True), F("outtime").desc(nulls_first = True),"-indate",'-intime')
    return render(request,'admindoctorsessionlogs.html',context={"doctorLogData":doctors})

# render patients
def adminpatients(request):
    activePatients = Patient.objects.filter(outdate = None ).order_by("-indate","-id")
    print(activePatients)
    
    return render(request,'adminpatients.html',context={"patients":activePatients})

# render patientshistory
def adminpatientshistory(request):
    allPatients = Patient.objects.all().order_by("-indate","-id")
    pastPatients = []
    for i in allPatients:
        if i.outdate != None:
            pastPatients.append(i)

    return render(request,'adminpatientshistory.html',context={"patients":pastPatients})

# render patientssearch
def adminpatientssearch(request):
    availablePatients = Patient.objects.filter(outdate = None ).order_by("-indate","-id")
    return render(request,'adminpatientssearch.html',context={'patients':availablePatients})

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



# render queries
def adminqueries(request):
    # load queries from databse 
    activeQuery = {"queries":Query.objects.filter(response = '')}
    return render(request,'adminqueries.html',context=activeQuery)

# sending response query
def send_response(request,id):
    if request.method == "POST":
       
        try:
            response_text = request.POST.get("answer")
            
            if not response_text:
                return redirect('adminqueries')
                
            else:
                queryData = Query.objects.get(id=id)
                queryData.response = response_text
                queryData.save()
            
        except:
            pass
    return redirect('adminqueries')

# render users
def adminusers(request):
    users = User.objects.all().order_by("-joindate")
    return render(request,'adminusers.html',context={"users":users})

# render usersessionlogs
def adminusersessionlogs(request):
    users = Userlogindata.objects.all().order_by(F("outdate").desc(nulls_first = True), F("outtime").desc(nulls_first = True))
    return render(request,'adminusersessionlogs.html',context={"userLogData":users})

# render doctor session logs
def adminlogout(request):
    adminSessionData = Adminlogindata.objects.get(aid = request.session["aid"], outtime__isnull = True)
    adminSessionData.outdate = timezone.now()
    adminSessionData.outtime = timezone.now()
    adminSessionData.save()
    del request.session['aid']
    request.session.modified = True 
    return redirect("adminlogin")


def adminDp(request):
    if request.method == "POST":
        pid = request.session.get("aid")
        ptype = "admin"
        image= request.FILES.get("dp")

        try:
            dp = Dp.objects.get(pid=int(pid),ptype=ptype)
            dp.image = image
            dp.save()
        except:
            Dp.objects.create(pid = int(pid),ptype=ptype,image=image)

    return redirect(admindashboard)