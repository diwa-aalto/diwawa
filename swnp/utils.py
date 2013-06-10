import zmq
import glob
import socket
import iptools
from awake import wol
import base64
import urllib2
import datetime
import os
from models import *
from django.db.models import Count
from datetime import timedelta
from django.conf import settings


IP_ADDR = getattr(settings, 'IP_ADDR', '')
MACS = getattr(settings, 'MACS', [])
PROJECTS_PATH = getattr(settings, 'PROJECTS_PATH', '/')

# Diwa TVs,port numbers and commands for SHARP 60LE636 IP control
TVS = [('192.168.1.100', 10002),
       ('192.168.1.101', 10002),
       ('192.168.1.102', 10002)
]
TV_COMMANDS = {'powr0':'POWR0   \r',
               'powr1':'POWR1   \r',
               'hdmi1':'IAVD4   \r'
}
     
def send_open_path(target, ip, path):
    """
    Send open path to target at ip.

    :param target: The target's wos id.
    :type target: String

    :param ip: IP address
    :type ip: Long

    :param path: File path
    :type path: String

    """
    try:
        context = zmq.Context() 
        socket = context.socket(zmq.REQ)
        socket.setsockopt(zmq.LINGER, 10)
        socket.connect('tcp://' + iptools.long2ip(ip) + ':5555')
        if target and ip and path:
            socket.send('open;' + target + ';' + str(path))
        socket.close()
        context.term()          
    except Exception, e:
        pass
        
        
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj 
     
       
def send_open_url(target, ip, url):
    """
    Send open url to target at ip.

    :param target: The target's wos id.
    :type target: String

    :param ip: IP address
    :type ip: Long

    :param url: URL
    :type url: String

    """
    try:
        context = zmq.Context() 
        socket = context.socket(zmq.REQ)
        socket.setsockopt(zmq.LINGER, 10)
        socket.connect('tcp://' + iptools.long2ip(ip) + ':5555')
        if target and ip and url:
            socket.send('url;' + target + ';' + str(url))       
        socket.close()
        context.term()          
    except Exception, e:
        pass
 
        
def awake():
    """
    Sends WakeOnLAN packet to the MAC addresses in MACS.
    Also, turns on TV's (SHARP IP control).

    """
    # send wol packet to the machines
    for mac in MACS:
        t = iter(mac)
        mac_s = ':'.join(a + b for a, b in zip(t, t))
        wol.wol(mac_s, broadcast='192.168.1.255')
    # turn on the tvs, switch to hdmi1
    for tv in TVS:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(tv)
            s.sendall(TV_COMMANDS['powr1'])
            s.recv(9)
            s.sendall(TV_COMMANDS['hdmi1'])
            s.recv(9)
            s.sendall(TV_COMMANDS['hdmi1'])
            s.recv(9)
            s.close()
        except Exception, e:
            pass  
            
                     
def snaphot(path):
    """
    Save a snapshot from the IP camera () to project's directory.

    :param path: Path to project's directory
    :type path: String

     """
    if path:
        path = os.path.join(PROJECTS_PATH,path[path.find('Projects') + 8:])
        path = os.path.join(path, 'Snapshots').replace('\\', '/')
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except:
            pass
        request = urllib2.Request("http://192.168.1.85/image/jpeg.cgi") # HTTP request
        base64string = base64.encodestring('%s:%s' % ('admin', 'wosadmin')).replace('\n', '') # Encode username and password
        request.add_header("Authorization", "Basic %s" % base64string)   # Add encoded credentials to the request
        event_id = str(Event.objects.all().order_by("-id")[0].id)
        try:
            data = urllib2.urlopen(request).read()
            name = event_id + '_' + datetime.datetime.now().strftime("%d%m%Y%H%M%S") + '.jpg'
            name = os.path.join(path, name)
            output = open(name, 'wb')
            output.write(data)
            output.close()
        except Exception:
            pass
        

def send_save_audio():
    """Send save audio message to responsive node."""
    nodes = Computer.objects.filter(time__gte=datetime.datetime.now() - timedelta(minutes=2), responsive=1).annotate(dcount=Count('name')).order_by('wos_id')
    for node in nodes[0:1]: 
        try:
            context = zmq.Context() 
            socket = context.socket(zmq.REQ)
            socket.setsockopt(zmq.LINGER, 10)
            socket.connect('tcp://' + iptools.long2ip(node.ip) + ':5555')
            socket.send('save_audio;0;0')       
            socket.close()
            context.term()          
        except Exception, e:
            pass
    

def send_screenshot():
    """Send screenshot message to SCREEN nodes."""
    nodes = Computer.objects.filter(time__gte=datetime.datetime.now() - timedelta(minutes=2), screens__gt=0).annotate(dcount=Count('name')).order_by('wos_id')
    for node in nodes: 
        try:
            context = zmq.Context() 
            socket = context.socket(zmq.REQ)
            socket.setsockopt(zmq.LINGER, 10)
            socket.connect('tcp://' + iptools.long2ip(node.ip) + ':5555')
            socket.send('screenshot;0;0')       
            socket.close()
            context.term()          
        except Exception, e:
            pass    
    
          
def send_command(command):
    """
    Send command to SCREEN nodes.

    :param command: The command to send
    :type command: String

    """
    nodes = Computer.objects.filter(time__gte=datetime.datetime.now() - timedelta(minutes=2), screens__gt=0).annotate(dcount=Count('name')).order_by('wos_id')
    for node in nodes: 
        try:
            context = zmq.Context() 
            socket = context.socket(zmq.REQ)
            socket.setsockopt(zmq.LINGER, 10)
            socket.connect('tcp://' + iptools.long2ip(node.ip) + ':5555')
            socket.send('command;0;%s' % command)       
            socket.close()
            context.term()          
        except Exception, e:
            pass
    
                                   
def ip_leases():
    """
    Return a list of IP address leases from ASUS RT-N56U router

    :rtype: list

    """
    request = urllib2.Request("http://192.168.1.1/device-map/clients.asp") # HTTP request
    base64string = base64.encodestring('%s:%s' % ('admin', 'wosadmin1')).replace('\n', '') # Encode username and pass 
    request.add_header("Authorization", "Basic %s" % base64string) # Add encoded username and pass to the request
    try:
        data = urllib2.urlopen(request).read()
        lindex = data.find('leases =')
        rindex = data.find(']]', lindex) + 2
        leases = data[lindex + 9:rindex]
        return eval(leases)
    except Exception:
        return [] 
    
    
def project_json_generate(dic):
    """
    Generates JSON from dict.

    :param dic: List of projects as dict instances.
    :type dic: List of dict instances

    :rtype: JSON String

    """
    json = u"{"
    for key in dic:
        d = dic[key]
        json += u'"' + key + '":'
        if isinstance(d, dict):
            d = [d]
        if key == "project":    
            json += u"{"
        else:
            json += u"["       
        for k in d:
            obj = key != "project"
            if obj:
                json += "{"
            for j in k:
                val = k[j]
                if hasattr(val, 'isoformat'):
                    val = val.isoformat()
                elif isinstance(val, unicode):
                    val = val.replace('"', '\"').replace('\\', '\\\\')
                elif isinstance(val, (int, long)):
                    val = str(val)
                else:
                    val = ''             
                k[j] = val
                json += u'"' + j + u'":' + u'"' + val + u'",'
            if json[-1:] == ',':
                json = json[:-1]
            json += "},"
        
        if json[-1:] == ',':
            json = json[:-1]
        if key == "project":  
            pass
        else:
            json += u"]" 
        json += u","
    json = json[:-1]    
    json += u"}"       
    return json    

          
def get_event_files(event_id, directory):
    """
    Fetches files related to an event from project's directory.

    :param event_id: Database row id of an event.
    :type event_id: Integer

    :param directory: The project directory.
    :rtype: String

    """
    idx = directory.find('Projects') + 9
    if idx == -1:
        return '[]'		
    directory = os.path.join(PROJECTS_PATH, directory[idx:]).replace('\\', '/')
    idx = directory.find('Projects') + 9
    os.chdir(directory)
    fs = glob.glob("*/%s_*" % (event_id))
    if 'C:' in os.getcwd():
        return str([os.path.join('/static/Projects', directory[idx:], f).encode('utf-8').replace('C:/', '/static/').replace("\\", "/") for f in fs]).replace("'", '"')
    return str([os.path.join('/static/Projects', directory[idx:], f).encode('utf-8').replace('share', 'static') for f in fs]).replace("'", '"')


def event_has_audio(event_id, directory):
    """
    Fetches audio files related to an event from project's directory.

    :param event_id: Database row id of an event.
    :type event_id: Integer

    :param directory: The project directory.
    :rtype: JSON String

    """
    idx = directory.find('Projects') + 9 
    if idx == -1:
        return '[]'        
    directory = os.path.join(PROJECTS_PATH, directory[idx:]).replace('\\', '/')
    idx = directory.find('Projects') + 9
    os.chdir(directory)
    fs = glob.glob("Audio/%s_*" % (event_id))
    json = {}
    for f in fs:
        json[os.path.splitext(f)[1][1:].encode('utf-8')] = os.path.join('/static/Projects', directory[idx:], f).encode('utf-8').replace('\\', '/')  
    return '[' + str(json).replace("'", '"') + ']'
