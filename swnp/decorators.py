import utils
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

GetOrCreate = User.objects.get_or_create

def custom_login(f):
    """ Login with a MAC address or Guest account."""
    def wrapper(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated():
            # User is not already authenticated,
            # try to find correct mac and login.
            leases = utils.ip_leases()
            ip = request.META['REMOTE_ADDR']
            if 'X-Forwarded-For' in request.META:
                ip = request.META['X-Forwarded-For']
            for lease in leases:
                if lease[2] == ip:
                    try:
                        (user, created) = GetOrCreate(User.objects,
                                                      username=lease[1],
                                                      first_name=lease[0])
                        if created:
                            user.set_password(user.username)
                            user.save()
                        user = authenticate(username=user.username,
                                            password=user.username)
                        login(args[0], user)
                    except Exception, e:
                        print str(e)    
                    break           
            if not request.user.is_authenticated():    
                # failed, login guest account
                user, created = User.objects.get_or_create(username='Guest')
                if created:
                    user.set_password(user.username)
                    user.save()
                user = authenticate(username=user.username,
                                    password=user.username)
                login(args[0], user)   
        return f(*args, **kwargs)
    return wrapper
