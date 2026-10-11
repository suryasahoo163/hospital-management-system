
from .models import Doctor
from hmsadmin.models import Dp
def doctorData(request):
    dp = None
    if request.session.get("did"):
        doctorData = Doctor.objects.get(id = int(request.session.get("did")))

        try:
            dp = Dp.objects.get(pid = int(request.session.get("did")),ptype = "doctor").image.url
        except:
            dp = None
        return {"doctorData":doctorData,"ddp":dp}
    return {"doctorData":None,"ddp":dp}