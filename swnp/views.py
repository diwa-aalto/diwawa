from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from models import *
from django.db.models import Count
import utils
import os
from datetime import datetime, timedelta
from jchat.models import Room
from django.core import serializers
import json
from django.forms.models import model_to_dict
from decorators import custom_login
from operator import itemgetter
from collections import Counter
from django.db.models import Q
IP_ADDR = "192.168.1.10"
UNSETTED = False
def get_activity():
    try:
        activity = Activity.objects.filter(active=True).latest('id')
    except Activity.DoesNotExist:
        activity = None
    return activity 
@custom_login   
@csrf_protect
def index(request,template):
    """time__gte=datetime.now()-timedelta(minutes=2),"""
    print request.get_full_path(), request.REQUEST
    print template
    ip = request.META['X-Forwarded-For'] if 'X-Forwarded-For' in request.META else request.META['REMOTE_ADDR']
    activity = get_activity()
    if activity:
        room = Room.objects.get_or_create(activity.project)
    else:    
        room = None
    if 'tab' in request.REQUEST:
        tab = request.REQUEST['tab']
    else:
        tab = "diwaweb"        
    projects = Project.objects.filter(company__id=1).order_by('name')        
    nodes = Computer.objects.filter(time__gte=datetime.now()-timedelta(minutes=2),screens__gt=0).annotate(dcount=Count('name')).order_by('wos_id')
    print nodes
    if not nodes:
        Activity.unset_all()
    node_list = []
    for node in nodes:
        path = '/share/screen_images/'+str(node.wos_id)+'.png'
        print node,path
        if os.path.isfile(path) or node.wos_id==245:
            node_list.append({'node':node,'img':'/static/screen_images/'+str(node.wos_id)+'.png'})
        else:
            node_list.append({'node':node,'img':'/static/screen_images/SCREEN.png'})    
    temp = 'index.html' if template=='norm' else 'metro.html'
    return render_to_response(temp,{'activity':activity,'tab':tab,'nodes':nodes,'chat_id':room.id if room else None,'node_list':node_list,'projects':projects},context_instance=RequestContext(request))
@custom_login   
@csrf_protect
def diwamb(request):
    """time__gte=datetime.now()-timedelta(minutes=2),"""
    projects = Project.objects.filter(company__id=1).order_by('name')
    activity = get_activity() 
    print "rendering"       
    return render_to_response('meetingbrowser.html',{'projects':projects,'activity':activity,'tab':'diwamb'},context_instance=RequestContext(request))

def project_timeline_json(request,id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        project = None
        
    if project:
        data = [{'type':'session','start':session.starttime,'end':session.endtime,'id':session.id,'name':session.name}for session in project.session_set.all()]
        data += [{'type':'fileaction','start':action.action_time,'id':action.id, 'action':action.action.name, 'path':os.path.basename(action.file.path),'ext':os.path.splitext(action.file.path)[1]}for action in  Fileaction.objects.filter(file__project=project).order_by('action_time')]
        actions = Fileaction.objects.filter(file__project=project).order_by('action_time').values('id','file','action','action_time')
        data += [{'type':'event','start':event.time,'id':event.id,'title':event.title,'desc':event.desc}for event in Event.objects.filter(session__project=project).order_by('time')]      
        events = Event.objects.filter(session__project=project).order_by('time').values('id','time','desc','title')    
        data_sorted = sorted(data, key=itemgetter('start'))      
        counts = [k for k,v in Counter(map(lambda x:x['start'],data_sorted)).items() if v > 1]
        print counts  
        return HttpResponse(json.dumps(data_sorted,default=utils.date_handler), mimetype='application/json')
    else:
        return HttpResponse('{}')  
    
def project_json(request,id):
    try:
        project = Project.objects.get(id=id)
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
    if 'event_id' in request.GET and 'project_id' in request.GET:
        event_id = request.GET['event_id']
        project_id = request.GET['project_id']
        print project_id,event_id,"event_files"
        return HttpResponse(utils.get_event_files(event_id, Project.objects.get(pk=project_id).dir), mimetype='application/json')
    return HttpResponse('{}', mimetype='application/json')
def has_audio(request):
    if 'event_id' in request.REQUEST:
        event_id = request.REQUEST['event_id']
        print "has event_id",event_id
        try:
            event = Event.objects.get(pk=event_id)
            project = event.session.project
        except:
            return HttpResponse("False")
        return HttpResponse(str(utils.event_has_audio(event_id,project.dir)))
    return HttpResponse("False")    
@csrf_protect
def project_select(request):
    response = "ERROR"
    if request.is_ajax() and request.method == 'POST' and 'id' in request.POST:
        project = Project.objects.get(id=request.POST['id'])
        print 'selected project',project
        activity = get_activity()
        if activity:
            activity.project = project
            activity.save()
            utils.send_project(int(project.id))
            response = 'OK'
    return HttpResponse(response)

@csrf_protect
def projects_json(request):
    projects = [model_to_dict(project) for project in Project.objects.all()]
    return HttpResponse(json.dumps(projects,default=utils.date_handler), mimetype='application/json')
    
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
    print str(activity)
    if request.is_ajax() and request.method == 'POST' and activity:
        
        title=None 
        if 'title' in request.POST:
            title=request.POST['title'] 
        try:
            if activity:
                session = activity.session
            else:
                session = None    
            e = Event(title=title,session=session)
            e.save()
            project_path = activity.project.dir if activity else '\\\\192.168.1.10\\Pictures'
            utils.snaphot(project_path)
            utils.send_screenshot()
            utils.send_save_audio()
            response = "OK"
        except Exception,err:
            print "error:",str(err)       
    return HttpResponse(response)   
@custom_login  
@csrf_protect
def chat(request):
    activity = get_activity()
    if activity:
        room = Room.objects.get_or_create(activity.project)
    else:    
        room = None   
    return render_to_response('chat.html',{'activity':activity,'chat_id':room.id if room else None},context_instance=RequestContext(request))
def awake(request):
    if request.method == 'GET':
        utils.awake()
        return HttpResponse('OK')
    return HttpResponse('ERROR') 
    
def ipcamera(request,command):
    response = ''
    if command == 'start':
        response = utils.save_ipcamera_stream()
    elif command == 'stop':
        response = utils.stop_ipcamera_stream()    
    return HttpResponse(response)
   
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
        #nodes = Computer.objects.filter(wos_id__gte=2,wos_id__lte=4).annotate(dcount=Count('name')).order_by('wos_id')
        print nodes
        try:
            if not nodes and not UNSETTED:
                UNSETTED = True
                Activity.unset_all()
            elif nodes:
                UNSETTED = False    
            node_list = []
        except Exception, e:
            print str(e)
        node_list = []    
        for node in nodes:
            #path = '\\\\192.168.1.10\\static\\screen_images\\'+str(node.wos_id)+'.png'
            path = os.path.join('/share/SCREEN_IMAGES/',str(node.wos_id)+'.png')
            print node,path
            if os.path.isfile(path):
                node_list.append({'node':model_to_dict(node),'img':'/static/screen_images/'+str(node.wos_id)+'.png'})
            else:
                node_list.append({'node':model_to_dict(node),'img':'/static/screen_images/SCREEN.png'})    
        json_serializer = serializers.get_serializer("json")()
        response =  json_serializer.serialize(nodes, ensure_ascii=False, indent=2, use_natural_keys=True)
        return HttpResponse(json.dumps(node_list,default=utils.date_handler), mimetype='application/json')
    else:
        return HttpResponse(json.dumps({'status':'error'}), mimetype='application/json')

    #return render_to_response('nodes.html',{'activity':activity,'nodes':nodes,'node_list':node_list},context_instance=RequestContext(request))
                       
@csrf_protect
def upload(request,id):
    path = "//share//Projects//temp"
    #path = "C:\\temp"
    try:
        activity = Activity.objects.filter(active=True).latest('id')
        path = activity.project.dir
    except Activity.DoesNotExist:
        pass 
    print "upload started",id,type(id)
    try:
        if int(id):
            c = Computer.objects.get(id=id)	
        if request.is_ajax() and request.method == 'POST':
            print "post keys"
            uploaded_path = None
            for key, value in request.POST.iteritems() :
                print key, value
            if 'file' in request.POST:
                print "only file link"
                send_path = [request.POST['file'].encode('iso-8859-1').replace('/share','\\\\192.168.1.10')]
                print send_path
            else:    
                print request.FILES
                uploaded_path = handle_uploaded_file(request.FILES,path)
                
            if uploaded_path:
                print "uploaded path"
                send_path = [w.replace('//share','\\\\'+IP_ADDR) for w in uploaded_path]
                send_path = [w.replace('//','\\') for w in send_path]
            if int(id):    	
                
                if 'file' in request.POST:
                    send_path = [w.replace('/share','\\\\'+IP_ADDR) for w in send_path]
                    send_path = [w.replace('//','\\') for w in send_path]
                    send_path = [w.replace('/','\\') for w in send_path]
                print "sending files to",str(c.wos_id),send_path
                utils.send_open_path(str(c.wos_id),c.ip,send_path)
            return HttpResponse('SUCCESS')
    except Exception,e:
        print "error",str(e)
        return HttpResponse('ERROR')
@csrf_protect
def openurl(request,id):
        c = Computer.objects.get(id=id)    
        if request.is_ajax() and request.method == 'POST':
            if 'url' in request.POST:
                url = request.POST['url'].encode('utf-8')
                print "open url",str(c.wos_id),url
                utils.send_open_url(str(c.wos_id),c.ip,url)
                return HttpResponse('SUCCESS')
        print "error"
        return HttpResponse('ERROR')
    
def handle_uploaded_file(files,path):
    uploaded_files = []
    for filename, f in files.iteritems():
        try:
            full_path = os.path.join(path,str(f))
            full_path = path+'\\'+str(f)
            fixed_path = '/share/Projects/'+full_path[full_path.find('Projects')+9:]
            fixed_path = fixed_path.replace('\\','/')
            print full_path,fixed_path
            with open(fixed_path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            uploaded_files.append(full_path)
        except Exception, e:
            print e
            with open('log.txt','wb+') as log:
		log.write(str(e))		
            return False
    print "all done",str(uploaded_files)  
    return uploaded_files      
#
# jQuery File Tree
# Python/Django connector script
# By Martin Skou
#
import os
import urllib

def dirlist(request):
    p = "/share/Projects/"
    r=['<ul class="jqueryFileTree" style="display: none;">']
    try:
        r=['<ul class="jqueryFileTree" style="display: none;">']
        d=urllib.unquote(request.POST.get('dir','c:\\temp')) 
        print d   
        da = d[d.rfind("\\"):]
        print da
        while da.startswith("\\") or da.startswith("/"):
            da = da[1:]
        d = os.path.join(p,d[d.find('Projects')+9:]).replace('\\','/')
        print d
        for f in os.listdir(d):
            ff=os.path.join(d,f)
            if os.path.isdir(ff):
                r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
            else:
                e=os.path.splitext(f)[1][1:] # get .ext and remove dot
                r.append('<li class="file ext_%s"><a href="#" rel="%s" draggable="true" ondragstart="drag(event)">%s</a></li>' % (e,ff,f))
        r.append('</ul>')
    except Exception,e:
        r.append('Could not load directory(%s): %s' % (d,str(e)))
    r.append('</ul>')
    return HttpResponse(''.join(r))

@csrf_protect
def snapshot(request):
    response = "ERROR"
    activity = get_activity()
    if request.method == 'GET':
        try:
            project_path = activity.project.dir if activity else '\\\\'+IP_ADDR+'\\Public'
            utils.snaphot(project_path)
            response = 'OK'
        except Exception,e:
            print str(e)
    return HttpResponse(response)  
@csrf_protect
def screenshot(request):
    response = "ERROR"
    activity = get_activity()
    if request.is_ajax() and request.method == 'GET' and activity:
        try:
            utils.send_screenshot()
            response = 'OK'
        except Exception,e:
            print str(e)
    return HttpResponse(response)           
