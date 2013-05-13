'''
Created on 19.9.2012

@author: neriksso
'''
import zmq
import glob
import json
import socket
import time
import iptools
from awake import wol
import base64
import urllib2
import datetime
import os
from subprocess import call
from models import *
from django.db.models import Count
from datetime import timedelta
PGM_IP="239.128.128.1:5555"
PREFIX_CHOICES = ['JOIN','LEAVE','SYNC','MSG','PING','PONG']
MACS = ['001999C7EE5A','001999BEFA22','001999BEFB76']
TVS = [('192.168.1.100',10002),('192.168.1.101',10002),('192.168.1.102',10002)]
TV_COMMANDS = {'powr0':'POWR0   \r','powr1':'POWR1   \r','hdmi1':'IAVD4   \r'}
class Message:
    """A class representation of a Message. 
    
    Messages are divided into three parts: TAG, PREFIX, PAYLOAD. Messages are encoded to json for transmission. 
    
    :param TAG: TAG of the message.
    :type TAG: String.
    :param PREFIX: PREFIX of the message.
    :type PREFIX: String.
    :param PAYLOAD: PAYLOAD of the message.
    :type PAYLOAD: String.
    
    """
    def __init__(self,TAG,PREFIX,PAYLOAD):
        self.TAG=TAG
        if PREFIX in PREFIX_CHOICES:
            self.PREFIX=PREFIX
        else:
            raise TypeError
        self.PAYLOAD=PAYLOAD
    def to_dict(msg):
        """Return a message in a dict.
        
        :param msg: The message.
        :type msg: :class:`swnp.Message`
        :rtype: Dict.
        
        """
        return {'TAG':msg.TAG,'PREFIX':msg.PREFIX,'PAYLOAD':msg.PAYLOAD}
    to_dict = staticmethod(to_dict)
    def from_json(json_dict):
        """Return a message from json.
        
        :param json_dict: The json.
        :type json_dict: json.
        :rtype: :class:`swnp.Message`.
        
        """
        return Message(json_dict['TAG'].encode('utf-8'),json_dict['PREFIX'].encode('utf-8'),json_dict['PAYLOAD'].encode('utf-8'))
    from_json = staticmethod(from_json)
    
    def __str__(self):
        return "_".join([self.TAG,self.PREFIX,self.PAYLOAD])
    
    def __repr__(self):
        return "_".join([self.TAG,self.PREFIX,self.PAYLOAD])
    
def get_local_ip_address(target):
    ipaddr = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((target, 8000))
        ipaddr = s.getsockname()[0]
        s.close()
    except:
        ipaddr = None
    return ipaddr
     
def send_open_path(target,ip,path):
    print "sending open path"
    try:
        context = zmq.Context() 
        #ip = get_local_ip_address('www.google.com')
        socket =  context.socket(zmq.REQ)
        socket.setsockopt(zmq.LINGER, 10)
        print 'ip',iptools.long2ip(ip)
        socket.connect('tcp://'+iptools.long2ip(ip)+':5555')
        if target and ip and path:
            socket.send('open;'+target+';'+str(path))
        socket.close()
        context.term()          
    except Exception,e:
        print "error",str(e)
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj        
def send_open_url(target,ip,url):
    print "sending open url"
    try:
        context = zmq.Context() 
        #ip = get_local_ip_address('www.google.com')
        socket =  context.socket(zmq.REQ)
        socket.setsockopt(zmq.LINGER, 10)
        print 'ip',iptools.long2ip(ip)
        socket.connect('tcp://'+iptools.long2ip(ip)+':5555')
        if target and ip and url:
            socket.send('url;'+target+';'+str(url))       
        socket.close()
        context.term()          
    except Exception,e:
        print "error",str(e)
def save_ipcamera_stream():
    save_cmd = ['TERMINFO=\'/usr/share/terminfo/\'', 'screen', '-dmS', 'ipcamera', 'ffmpeg', '-i', 'rtsp://192.168.1.85/play2.sdp', '-acodec', 'mp2', '-ab', '64k', '-y', '-vcodec', 'mpeg4', '-f', 'mp4', '/share/Projects/`date +%F_%T`.mp4']
    check_cmd = ['ps','ax','|','grep','-c','ffmpeg','-i']
    try:
        print "execuring:",' '.join(save_cmd)
        call(save_cmd)
        print "execuring:",' '.join(check_cmd)
        result = call(check_cmd)
        if result > 1:
            return "OK"
    except: 
        pass
    return "ERROR"

def stop_ipcamera_stream():
    kill_cmd = ['kill', '-2', '`pidof', 'ffmpeg`']
    check_cmd = ['ps','ax','|','grep','-c','ffmpeg','-i']
    try:
        print "execuring:",' '.join(check_cmd)
        result = call(check_cmd)
        if result > 1:
            print "execuring:",' '.join(kill_cmd)
            call(kill_cmd)
            print "execuring:",' '.join(check_cmd)
            result = call(check_cmd)
            if result > 1:
                return "OK"
            else:
                return "ERROR"
        return "OK"
    except:
        return "ERROR"
        
def awake():
    # send wol packet to the machines
    for mac in MACS:
        t = iter(mac)
        mac_s = ':'.join(a+b for a,b in zip(t, t))
        print mac_s
        wol.wol(mac_s,broadcast='192.168.1.255')
    # turn on the tvs, switch to hdmi1
    for tv in TVS:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect(tv)
            s.sendall(TV_COMMANDS['powr1'])
            s.recv(9)
            s.sendall(TV_COMMANDS['hdmi1'])
            s.recv(9)
            s.sendall(TV_COMMANDS['hdmi1'])
            s.recv(9)
            s.close()
        except Exception,e:
            print str(e)           
def snaphot(path):
    #path = '\\\\192.168.1.10\\Pictures\\Snapshots'
    #path = 'C:\\snapshots'
    path = os.path.join(path,'Snapshots').replace('\\\\192.168.1.10','/share').replace('\\','/')
    print path
    try:
	if not os.path.exists(path):
            os.makedirs(path)
    except:
        pass
    request = urllib2.Request("http://192.168.1.85/image/jpeg.cgi")
    base64string = base64.encodestring('%s:%s' % ('admin', 'wosadmin')).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)   
    event_id = str(Event.objects.all().order_by("-id")[0].id)
    try:
        data = urllib2.urlopen(request).read()
        name = event_id+'_'+datetime.datetime.now().strftime("%d%m%Y%H%M%S")+'.jpg'
        name = os.path.join(path,name)
        print 'Snaphot filename:'+name
        output = open(name,'wb')
        output.write(data)
        output.close()
    except Exception,e:
        print "Snapshot exception:"+str(e) 
def send_save_audio():
    nodes = Computer.objects.filter(time__gte=datetime.datetime.now()-timedelta(minutes=2),screens__gt=0).annotate(dcount=Count('name')).order_by('wos_id')
    for node in nodes[0:1]: 
        try:
            context = zmq.Context() 
            socket =  context.socket(zmq.REQ)
            socket.setsockopt(zmq.LINGER, 10)
            socket.connect('tcp://'+iptools.long2ip(node.ip)+':5555')
            socket.send('save_audio;0;0')       
            socket.close()
            context.term()          
        except Exception,e:
            print "error",str(e)
    print 'save_audio sent to %s' % nodes[0]		
def send_screenshot():
    print "sending screenshot"
    nodes = Computer.objects.filter(time__gte=datetime.datetime.now()-timedelta(minutes=2),screens__gt=0).annotate(dcount=Count('name')).order_by('wos_id')
    for node in nodes: 
        try:
            context = zmq.Context() 
            socket =  context.socket(zmq.REQ)
            socket.setsockopt(zmq.LINGER, 10)
            socket.connect('tcp://'+iptools.long2ip(node.ip)+':5555')
            socket.send('screenshot;0;0')       
            socket.close()
            context.term()          
        except Exception,e:
            print "error",str(e)
    print 'screenshot sent to %d nodes' % len(nodes) 
def send_project(project_id):
    nodes = Computer.objects.filter(time__gte=datetime.datetime.now()-timedelta(minutes=2),screens__gt=0).annotate(dcount=Count('name')).order_by('wos_id')
    for node in nodes: 
        try:
            context = zmq.Context() 
            socket =  context.socket(zmq.REQ)
            socket.setsockopt(zmq.LINGER, 10)
            socket.connect('tcp://'+iptools.long2ip(node.ip)+':5555')
            socket.send('project;%d;0' % project_id)       
            socket.close()
            context.term()          
        except Exception,e:
            print "error",str(e)
    print 'screenshot sent to %d nodes' % len(nodes) 
          
def send_command(command):
    nodes = Computer.objects.filter(time__gte=datetime.datetime.now()-timedelta(minutes=2),screens__gt=0).annotate(dcount=Count('name')).order_by('wos_id')
    for node in nodes: 
        try:
            context = zmq.Context() 
            socket =  context.socket(zmq.REQ)
            socket.setsockopt(zmq.LINGER, 10)
            socket.connect('tcp://'+iptools.long2ip(node.ip)+':5555')
            socket.send('command;0;%s' % command)       
            socket.close()
            context.term()          
        except Exception,e:
            print "error",str(e)
    print 'screenshot sent to %d nodes' % len(nodes)                               
def ip_leases():
    request = urllib2.Request("http://192.168.1.1/device-map/clients.asp")
    base64string = base64.encodestring('%s:%s' % ('admin', 'wosadmin1')).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)   
    try:
        data = urllib2.urlopen(request).read()
        lindex = data.find('leases =')
        rindex = data.find(']]',lindex)+2
        leases = data[lindex+9:rindex]
        return eval(leases)
    except Exception,e:
        return [] 
def project_json_generate(dic):
    json= u"{"
    for key in dic:
        d = dic[key]
        json+=u'"'+key+'":'
        if isinstance(d,dict):
            d = [d]
        if key=="project":    
            json+=u"{"
        else:
            json+=u"["       
        for k in d:
            #json+=u'"'+k+u'"'
            obj= key!="project"
            if obj:
                json+="{"
            for j in k:
                val = k[j]
                if hasattr(val,'isoformat'):
                    val = val.isoformat()
                elif isinstance(val,unicode):
                    val = val.replace('"','\"').replace('\\','\\\\')
                elif isinstance(val,(int,long)):
                    val = str(val)
                elif val is None:
                    val = ''    
                else:
                    print val, type(val)            
                k[j] = val
                json+=u'"'+j+u'":'+u'"'+val+u'",'
            if json[-1:] == ',':
                json = json[:-1]
            json+="},"
        
        if json[-1:] == ',':
            json = json[:-1]
        if key=="project":  
            pass
        else:
            json+=u"]" 
        json+=u","
    json=json[:-1]    
    json += u"}"    
    #print type(json),json      
    return json              
def get_event_files(event_id, dir):
    idx = dir.find('Projects')
    print idx	
    if idx == -1:
 	      return '[]'		
    dir = os.path.join('/share',dir[idx:]).replace('\\','/')
    #dir = os.path.join('C:/',dir[idx:]).replace('\\','/')
    print event_id, dir,"*/%s_"%(event_id)	
    os.chdir(dir)
    print os.getcwd()
    fs = glob.glob("*/%s_*"%(event_id))
    print fs
    if 'C:' in os.getcwd():
        return str([os.path.join(dir,file).encode('ascii').replace('C:/','/static/').replace("\\","/") for file in fs]).replace("'",'"')
    return str([os.path.join(dir,file).encode('ascii').replace('share','static') for file in fs]).replace("'",'"')
def event_has_audio(event_id, dir):
    idx = dir.find('Projects')  
    if idx == -1:
        return '[]'        
    #dir = os.path.join('C:/',dir[idx:]).replace('\\','/')
    dir = os.path.join('/share',dir[idx:]).replace('\\','/')
    print event_id, dir,"*/%s_"%(event_id)    
    os.chdir(dir)
    print os.getcwd()
    fs = glob.glob("Audio/%s_*"%(event_id))
    json = {}
    for f in fs:
        json[os.path.splitext(f)[1][1:].encode('utf-8')]=os.path.join('/static/Projects',dir[idx+1:],f).encode('utf-8').replace('\\','/')
    print json    
    return '['+str(json).replace("'",'"')+']'
