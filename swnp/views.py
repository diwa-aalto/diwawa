from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from models import (Activity, Project, Session, Event, Fileaction, Computer,
                    File)
from django.db.models import Count, F, Q
from datetime import datetime, timedelta
from jchat.models import Room
from django.forms.models import model_to_dict
from decorators import custom_login
from django import forms
from django.contrib import messages
from django.conf import settings
import utils
import os
import sys
import urllib
import json

IP_ADDR = getattr(settings, 'IP_ADDR', '192.168.1.10')
PROJECTS_PATH = getattr(settings, 'PROJECTS_PATH', '/')
SCREEN_IMAGES = getattr(settings, 'SCREEN_IMAGES', '/')
STATIC_PATHS = getattr(settings, 'STATICFILES_DIRS', '/')
STATIC_PATH = STATIC_PATHS[0]
TEMP_DIR = getattr(settings, 'TEMP_DIR', '/')
UNSETTED = False


def get_activity():
    """
    Fetches the active activity for PGM_GROUP 1
    
    :rtype: Activity

    """
    try:
        activity = Activity.objects.filter(active=1).latest('id')
    except Activity.DoesNotExist:
        activity = None
    return activity

 
@custom_login   
@csrf_protect
def index(request):
    activity = get_activity()
    activeProject = None
    if activity:
        activeProject = activity.project
        room = Room.objects.get_or_create(activeProject)
    else:    
        room = None
        
    if 'tab' in request.REQUEST:
        tab = request.REQUEST['tab']
    else:
        tab = 'diwaweb'

    projects = []
    for p in Project.objects.filter(company__id=1).order_by('name'):
        if (activeProject) and (p.id == activeProject.id):
            projects.append(p)
            continue
        if (p.password == None) or (len(p.password) < 1):
            projects.append(p)
    result = None
    try:
        result = render_to_response(
               "metro.html",
                   {'activity': activity,
                    'tab': tab,
                    'nodes': nodes,
                    'chat_id': room.id if room else None,
                    'projects': projects
                    },
                context_instance=RequestContext(request)
            )
    except Exception, e:
        raise e
    return result


@custom_login   
@csrf_protect
def diwamb(request):
    activeProject = None
    activity = get_activity()
    if activity:
        activeProject = activity.project
    projects = []
    for p in Project.objects.filter(company__id=1).order_by('name'):
        if (activeProject) and (p.id == activeProject.id):
            projects.append(p)
            continue
        if (p.password == None) or (len(p.password) < 1):
            projects.append(p)
    return render_to_response(
              'meetingbrowser.html',
                  {'projects': projects,
                   'activity': activity,
                   'tab': 'diwamb'
                   },
               context_instance=RequestContext(request)
    )


def project_json(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        project = None
        
    if project:
        sessions = list(project.session_set.all().extra(where=['endtime-starttime>60']).values('id','starttime','endtime','name'))
        actions = list(Fileaction.objects.filter(Q(file__project=project)|Q(session__project=project)).exclude(Q(file__path__icontains='Snapshots')|Q(file__path__icontains='Audio')|Q(file__path__icontains='Screenshots')).order_by('action_time').values('id','file__path','file__id','action__name','action_time'))
        events = list(Event.objects.filter(session__project=project,time__isnull=False).order_by('time').values('id','time','desc','title'))
        json_dict = {'project':model_to_dict(project),'sessions':sessions,'fileactions':actions,'events':events}
        return HttpResponse(utils.project_json_generate(json_dict), mimetype='application/json')
    else:
        return HttpResponse('{}')            


def event_files(request):
    if 'event_id' in request.GET:
        event_id = request.GET['event_id']
        project_id = Event.objects.get(pk=event_id).session.project.id
        return HttpResponse(utils.get_event_files(event_id, Project.objects.get(pk=project_id).dir), mimetype='application/json')
    return HttpResponse('{}', mimetype='application/json')


def has_audio(request):
    if 'event_id' in request.REQUEST:
        event_id = request.REQUEST['event_id']
        try:
            event = Event.objects.get(pk=event_id)
            project = event.session.project
            return HttpResponse(str(utils.event_has_audio(event_id,project.dir)))
        except:
            pass      
    return HttpResponse("False")    


@csrf_protect
def projects_json(request):
    activeProject = None
    activity = get_activity()
    if activity:
        activeProject = activity.project
    projects = []
    for p in Project.objects.filter(company__id=1).order_by('name'):
        if (activeProject) and (p.id == activeProject.id):
            projects.append(model_to_dict(p))
            continue
        if (p.password == None) or (len(p.password) < 1):
            projects.append(model_to_dict(p))
    # sys.stderr.write('My projects: ' + str([p for p in projects]) + '\n')
    # sys.stderr.flush()
    return HttpResponse(json.dumps(projects, default=utils.date_handler),
                        mimetype='application/json')

    
@csrf_protect
def shutdown(request):
    response = "ERROR"
    if request.method == 'GET':
        utils.send_command('shutdown /p')
        response = 'OK'
    return HttpResponse(response)       


@csrf_protect
def event(request):
    response = "ERROR"
    activity = get_activity()
    if request.is_ajax() and request.method == 'POST' and activity:    
        title=None 
        if 'title' in request.POST:
            title=request.POST['title'].strip() 
        try:
            if activity:
                session = activity.session
            else:
                session = None  
            e = Event(title=title,session=session)
            e.save()
            project_path = activity.project.dir if activity else None
            utils.snaphot(project_path, e.id)
            utils.send_screenshot()
            utils.send_save_audio()
            response = "OK"
        except Exception as e:
            print e    
    return HttpResponse(response)   


@custom_login  
@csrf_protect
def chat(request):
    activity = get_activity()
    if activity:
        room = Room.objects.get_or_create(activity.project)
    else:    
        room = None   
    return render_to_response('chat.html', {'activity':activity,'chat_id':room.id if room else None}, context_instance=RequestContext(request))


def awake(request):
    if request.method == 'GET':
        utils.awake()
        return HttpResponse('OK')
    return HttpResponse('ERROR') 
    

@csrf_protect
def activity(request): 
    if request.is_ajax() and request.method == 'GET':
        activity = get_activity()
        if activity:
            room = Room.objects.get_or_create(activity.project)
        else:    
            room = None
        result = {'status':'OK','room':room.id if room else 0,'project':model_to_dict(activity.project) if activity and activity.project else 0,'session':model_to_dict(activity.session) if activity and activity.session else 0}
        return HttpResponse(json.dumps(result,default=utils.date_handler), mimetype='application/json')
    else:
        return HttpResponse(json.dumps({'status':'error'}), mimetype='application/json')
    

@csrf_protect
def nodes(request): 
    if request.is_ajax() and request.method == 'GET':
        global UNSETTED
        nodes = Computer.objects.filter(time__gte=datetime.now()-timedelta(seconds=15),screens__gt=0).annotate(dcount=Count('name')).order_by('wos_id')   
        if not nodes:
            Activity.unset_all()  
        node_list = []
        for node in nodes:
            screens = SCREEN_IMAGES
            path = screens + os.sep + str(node.wos_id) + '.png'
            if os.sep != '/':
                path = path.replace('/', os.sep)
            if os.path.isfile(path):
                node_list.append({'node':model_to_dict(node),'img': '/static/screen_images/' + str(node.wos_id) + '.png'})
            else:
                node_list.append({'node':model_to_dict(node),'img': '/static/img/SCREEN.png'})
        return HttpResponse(json.dumps(node_list,default=utils.date_handler), mimetype='application/json')
    else:
        return HttpResponse(json.dumps({'status':'error'}), mimetype='application/json')


@csrf_protect
def upload(request, computer_id):
    path = TEMP_DIR
    try:
        activity = Activity.objects.filter(active=True).latest('id')
        path = activity.project.dir
    except Activity.DoesNotExist:
        pass 
    try:
        if int(computer_id):
            c = Computer.objects.get(pk=computer_id)
        if request.is_ajax() and request.method == 'POST':
            uploaded_path = None
            if 'file' in request.POST:
                # We are handling a file link
                send_path = [request.POST['file'].encode('utf-8')]
            else:    
                # We are uploading files
                uploaded_path = handle_uploaded_file(request.FILES,path)
                send_path = [w.replace(PROJECTS_PATH[:PROJECTS_PATH.find('Projects')],'\\\\'+IP_ADDR).replace('/','\\') for w in uploaded_path]
            if c:
                if 'file' in request.POST and IP_ADDR != "127.0.0.1":
                    send_path = [w.replace(PROJECTS_PATH[:PROJECTS_PATH.find('Projects')],'\\\\'+IP_ADDR).replace('/','\\') for w in send_path]
                utils.send_open_path(str(c.wos_id),c.ip,send_path)
                return HttpResponse('SUCCESS')
    except:
        pass
    return HttpResponse('ERROR')
    
    
@csrf_protect
def openurl(request,computer_id):
        c = Computer.objects.get(pk=computer_id)    
        if request.is_ajax() and request.method == 'POST':
            if 'url' in request.POST:
                url = request.POST['url'].encode('utf-8')
                utils.send_open_url(str(c.wos_id), c.ip, url)
                return HttpResponse('SUCCESS')
        return HttpResponse('ERROR')

    
def handle_uploaded_file(files,path):
    uploaded_files = []
    for filename, f in files.iteritems():
        try:
            full_path = os.path.join(path,unicode(f))
            fixed_path = os.path.join(PROJECTS_PATH,full_path[full_path.find('Projects')+9:]).replace('\\','/')
            with open(fixed_path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            uploaded_files.append(full_path)
        except Exception:	
            return False 
    return uploaded_files      


def dirlist(request):
    """
    jQuery File Tree
    Python/Django connector script
    By Martin Skou

    """
    r = ['<ul class="jqueryFileTree" style="display: none;">']
    try:
        r = ['<ul class="jqueryFileTree" style="display: none;">']
        d = urllib.unquote(request.POST.get('dir', TEMP_DIR))
        da = d[d.rfind("\\"):]
        while da.startswith("\\") or da.startswith("/"):
            da = da[1:]
        d = unicode(os.path.join(PROJECTS_PATH, d[d.find('Projects') + 9:]))
        d = d.replace('\\', os.sep).replace('/', os.sep)
        if os.name == 'nt':
            d = r'\\' + d
        for f in os.listdir(d):
            ff = os.path.join(d, f)
            if os.path.isdir(ff):
                r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
            else:
                e=os.path.splitext(f)[1][1:] # get .ext and remove dot
                r.append('<li class="file ext_%s"><a href="#" rel="%s" draggable="true" ondragstart="drag(event)">%s</a></li>' % (e,ff,f))
        r.append('</ul>')
    except Exception,e:
        r.append('Could not load directory(%s): %s' % (d, str(e)))
    r.append('</ul>')
    return HttpResponse(''.join(r))

@csrf_protect
def snapshot(request):
    response = "ERROR"
    activity = get_activity()
    if request.method == 'GET' and activity.project and activity.session:
        try:
            project_path = activity.project.dir
            utils.snaphot(project_path)
            response = 'OK'
        except Exception:
            pass
    return HttpResponse(response)

  
@csrf_protect
def screenshot(request):
    response = "ERROR"
    activity = get_activity()
    if request.is_ajax() and request.method == 'GET' and activity:
        try:
            utils.send_screenshot()
            response = 'OK'
        except Exception:
            pass
    return HttpResponse(response) 


class EventForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Event
        fields = ['title']


@csrf_protect
def edit_event(request,event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(instance=event,initial={'desc':event.desc})
    if request.method == 'POST':
        # Handle form submit
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            event.desc = form.cleaned_data['desc']
            event.save()
            messages.success(request, 'Event details saved.')
        else:
            messages.error(request, "The form is not valid.")    
    return render_to_response("edit_event.html", {'event':event, 'form':form}, context_instance=RequestContext(request))

@csrf_protect
def stats(request):
    """
    Creates statistics listing of the projects.

    The project list does not contain password protected projects,
    except if one is currently on.

    The sessions list is filtered out of sessions whose duration is less
    than or equal to 3 minutes.

    """
    stats = []
    activeProject = None
    activity = get_activity()
    if activity:
        activeProject = activity.project
    projects = Project.objects.filter(company__id=1).order_by('name')
    for p in projects:
        isCurrent = (activeProject != None) and (p.id == activeProject.id)
        # If this is NOT the currently selected project...
        if (not isCurrent) or (not activeProject):
            # If this project is password protected, skip it.
            if (p.password != None) and (len(p.password) > 0):
                continue
        sessions = Session.objects.filter(project=p,
                                          endtime__gt=F('starttime') +
                                          timedelta(minutes=3))
        files = File.objects.filter(project=p)
        fileactions = Fileaction.objects.filter(file__in=files)
        events = Event.objects.filter(session__in=sessions)
        sQuery = {
            'avg': 'SUM(TIMESTAMPDIFF(SECOND, starttime, endtime)) / COUNT(*)',
            'min': 'MIN(TIMESTAMPDIFF(SECOND, starttime, endtime))',
            'max': 'MAX(TIMESTAMPDIFF(SECOND, starttime, endtime))',
            'count': 'COUNT(*)'
        }
        sessions = sessions.extra(select=sQuery)
        sessions = sessions.values_list('avg', 'min', 'max', 'count').get()
        session_average_duration = 0
        session_min_duration = 0
        session_max_duration = 0
        if sessions[0] is not None:
            session_average_duration = int(sessions[0])
        if sessions[1] is not None:
            session_min_duration = int(sessions[1])
        if sessions[2] is not None:
            session_max_duration = int(sessions[2])
        session_count = sessions[3]
        statsdata = {
            'selected': isCurrent,
            'name': p.name,
            'session_average_duration': session_average_duration,
            'session_min_duration': session_min_duration,
            'session_max_duration': session_max_duration,
            'session_count': session_count,
            'file_count': files.count(),
            'fileaction_count': fileactions.count(),
            'event_count': events.count()
        }
        stats.append(statsdata)
    return render_to_response(
                              'stats.html',
                              {
                                  'stats': stats,
                                  'tab': 'stats'
                              },
                              context_instance=RequestContext(request)
                              )

