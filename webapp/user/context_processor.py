
from .models import User
from hmsadmin.models import Dp
def userData(request):
    if request.session.get("uid"):
        userData = User.objects.get(id = int(request.session.get("uid")))
        try:
            dp = Dp.objects.get(pid=int(request.session.get("uid")), ptype="user").image.url
        except:
            dp = None
        return {"userData":userData,"dp":dp}
    return {"userData":None,"dp":None}