import utils
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def custom_login(f):
    """ Login with a MAC address or Guest account."""
    def wrapper(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated():
            #User is not already authenticated, try to find correct mac and login.
            leases = utils.ip_leases()
            ip = request.META['X-Forwarded-For'] if 'X-Forwarded-For' in request.META else request.META['REMOTE_ADDR']
            for lease in leases:
                if lease[2] == ip:
                    try:
                        user,created = User.objects.get_or_create(username=lease[1], first_name=lease[0])
                        if created:
                            user.set_password(user.username)
                            user.save()
                        user = authenticate(username=user.username, password=user.username)
                        login(args[0],user)
                    except Exception,e:
                        print str(e)    
                    break           
            if not request.user.is_authenticated():    
                # failed, login guest account
                user,created = User.objects.get_or_create(username='Guest')
                if created:
                    user.set_password(user.username)
                    user.save()
                user = authenticate(username=user.username,password=user.username)
                login(args[0],user)   
        return f(*args, **kwargs)
    return wrapper