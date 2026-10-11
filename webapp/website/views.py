from django.shortcuts import render,redirect
from django.http import JsonResponse
from user.models import Query, User, Userlogindata
from user.views import userdashboard
from django.utils import timezone
from doctor.models import Doctor,Doctorlogindata
from doctor.views import doctordashboard
from hmsadmin.models import Hmsadmin, Adminlogindata
from hmsadmin.views import admindashboard

message = None

def home(request):
    return render(request, 'index.html') # Adjust the path as needed


# render user login page
def userlogin(request):
    global message
    msg = [{"text":message}]
    message = None
    return render(request,'userlogin.html',context={"messages":msg})

# user registration page
def userregistration(request):
    return render(request,"userregistration.html")

# render doctor login page
def doctorlogin(request):
    global message
    msg = [{"text":message}]
    message = None
    return render(request,'doctorlogin.html',context={"message":msg})

# admin login page
def adminlogin(request):
    return render(request,'adminlogin.html')


def userquery(request):
    
    print(request.POST)
    print("---------------------------------")
    if request.method == "POST":
        
        name = str(request.POST.get("name")).title()
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        address = request.POST.get("address")
        query = request.POST.get("query")
       
        Query.objects.create(name=name,phone=phone,email=email,gender=gender,age=age,address=address,query=query)
        return redirect("home")
    return render(request,"index.html")

# user login authentication
def userAuth(request):
    global message
    try:
        id = int(request.session["uid"])
        
        phnid = User.objects.get(id = id).phone
       
        if phnid == int(str(request.POST["userId"]).strip(" ")):
            passwd = str(request.POST["password"])
            dData = User.objects.get(id = id).password
            if str(dData) == passwd:
                return redirect(userdashboard)

        else:
            return redirect(userlogin)
    except Exception as e:
        print(e)
    if request.method == "POST":
        loginId = request.POST['userId']
        try: # Checking if phone number exists
            loginId = int(str(loginId).strip(" "))

            if str(request.POST["password"]).strip(" ") == User.objects.get(phone = loginId).password: # matching password

                # creating session
                request.session["uid"] = User.objects.get(phone = loginId).id

                # removing the last login data
                try:
                    lastlog = Userlogindata.objects.get(uid = User.objects.get(id = int(request.session["uid"])),outdate__isnull=True)
                    lastlog.outdate = timezone.now()
                    lastlog.outtime = timezone.now()
                    lastlog.save()
                except Exception as e:
                    pass

                Userlogindata.objects.create(uid = User.objects.get(id = request.session["uid"]))
           
                request.session.set_expiry(0)
                
                return redirect(userdashboard)
            
            else:
                message = "Incorrect Password"
        except Exception as e:
            message = "Phone Number doesn't exits"
       
    return redirect(userlogin)


# doctor login authentication
def doctorAuth(request):
    global message
    try:
        id = int(request.session["did"])
        phnid = Doctor.objects.get(id = id).phone
       
        if phnid == int(str(request.POST["doctorId"]).strip(" ")):
            passwd = str(request.POST["password"])
            dData = Doctor.objects.get(id = id).password
            if str(dData) == passwd:
                return redirect(doctordashboard)

        else:
            return redirect(doctorlogin)
    except Exception as e:
        print(e)
    if request.method == "POST":
        loginId = request.POST['doctorId'] # phone no
        try: # Checking if phone number exists
            loginId = int(str(loginId).strip(" "))

            if str(request.POST["password"]) == Doctor.objects.get(phone = loginId).password: # matching password

                # creating session
                request.session["did"] = Doctor.objects.get(phone = loginId).id
                
                # removing the last login data
                try:
                    lastlog = Doctorlogindata.objects.get(did = Doctor.objects.get(id = int(request.session["did"])),outdate__isnull=True)
                    lastlog.outdate = timezone.now()
                    lastlog.outtime = timezone.now()
                    lastlog.save()
                except Exception as e:
                    print(e)
  

                Doctorlogindata.objects.create(did = Doctor.objects.get(id = request.session["did"]))
           
                request.session.set_expiry(0)
                return redirect(doctordashboard)
            
            else:
                message = "Incorrect Password"
        except Exception as e:
            message = "Phone Number doesn't exits"
       
    return redirect(doctorlogin)


def userRegistration(request):
    if request.method == "POST":
        name = str(request.POST["name"]).title()
        phone = request.POST["phone"]
        email = request.POST["email"]
        password = request.POST["password"]
        User.objects.create(name=name,phone=phone,email=email,password=password)
        return redirect(userlogin)
    return redirect(userRegistration)

def validateEP(request): #validate EP
    if request.method == "GET":
        phone = request.GET["phone"]
        email = request.GET["email"]

        try:
            user = User.objects.get(phone=phone)
            return JsonResponse({"message":"The Phone number already exists"})
        except:
            pass

        try:
            user = User.objects.get(email = email)
            return JsonResponse({"message":"The Email Address already exists"})
        except:
            return JsonResponse({"message":"allow"})
        

# Admin log in authentication
def adminAuth(request):
    global message
    try:
        id = int(request.session["aid"])
        phnid = Hmsadmin.objects.get(id = id).phone
       
        if phnid == int(str(request.POST["adminId"]).strip(" ")):
            passwd = str(request.POST["password"])
            dData = Hmsadmin.objects.get(id = id).password
            if str(dData) == passwd:
                return redirect(admindashboard)

        else:
            return redirect(adminlogin)
    except Exception as e:
        print(e)
    if request.method == "POST":
        loginId = request.POST['adminId'] # phone no
        try: # Checking if phone number exists
            loginId = int(str(loginId).strip(" "))

            if str(request.POST["password"]) == Hmsadmin.objects.get(phone = loginId).password: # matching password

                # creating session
                request.session["aid"] = Hmsadmin.objects.get(phone = loginId).id
                
                # removing the last login data
                try:
                    lastlog = Adminlogindata.objects.get(aid = Hmsadmin.objects.get(id = int(request.session["aid"])),outdate__isnull=True)
                    lastlog.outdate = timezone.now()
                    lastlog.outtime = timezone.now()
                    lastlog.save()
                except Exception as e:
                    print(e)
  

                Adminlogindata.objects.create(aid = Hmsadmin.objects.get(id = request.session["aid"]))
           
                request.session.set_expiry(0)
                return redirect(admindashboard)
            
            else:
                message = "Incorrect Password"
        except Exception as e:
            message = "Phone Number doesn't exits"
       
    return redirect(adminlogin)
