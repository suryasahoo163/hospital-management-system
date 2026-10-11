
from .models import Hmsadmin, Dp
def adminData(request):
    dp= None
    if request.session.get("aid"):
        adminData = Hmsadmin.objects.get(id = int(request.session.get("aid")))
        try:
            dp = Dp.objects.get(pid = int(request.session.get("aid")),ptype = "admin").image.url
        except:
            dp = None
        return {"adminData":adminData,"adp":dp}
    return {"adminData":None,"adp":dp}