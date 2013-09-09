""" Utility functions """
import zmq
import glob
import socket
import iptools
from awake import wol
import base64
import urllib2
import datetime
import os
import sys
from swnp.models import Computer
from django.db.models import Count
from datetime import timedelta
from django.conf import settings

IP_ADDR = getattr(settings, 'IP_ADDR', '')
MACS = getattr(settings, 'MACS', [])
PROJECTS_PATH = getattr(settings, 'PROJECTS_PATH', '/')
CAMERA_USERNAME = getattr(settings, 'CAMERA_USER', '')
CAMERA_PASSWORD = getattr(settings, 'CAMERA_PASSWORD', '')
ROUTER_USERNAME = getattr(settings, 'ROUTER_USER', '')
ROUTER_PASSWORD = getattr(settings, 'ROUTER_PASSWORD', '')

# Diwa TVs,port numbers and commands for SHARP 60LE636 IP control
TVS = [('192.168.1.100', 10002),
       ('192.168.1.101', 10002),
       ('192.168.1.102', 10002)
]

TV_COMMANDS = {'powr0':'POWR0   \r',
               'powr1':'POWR1   \r',
               'hdmi1':'IAVD4   \r'
}

def send_open_path(target, ip_addr, path):
    """
    Send open path to target at ip.

    :param target: The target's wos id.
    :type target: String

    :param ip_addr: IP address
    :type ip_addr: Long

    :param path: File path
    :type path: String

    """
    try:
        context = zmq.Context()
        sock = context.socket(zmq.REQ)
        sock.setsockopt(zmq.LINGER, 10)
        sock.connect('tcp://' + iptools.ipv4.long2ip(ip_addr) + ':5555')
        if target and ip_addr and path:
            sock.send('open;' + target + ';' + unicode(path).encode('utf-8'))
        sock.close()
        context.term()
    except Exception:
        pass


def date_handler(obj):
    """ JSON handler for Date objects"""
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def send_open_url(target, ip_addr, url):
    """
    Send open url to target at ip_addr.

    :param target: The target's wos id.
    :type target: String

    :param ip_addr: IP address
    :type ip_addr: Long

    :param url: URL
    :type url: String

    """
    try:
        context = zmq.Context()
        sock = context.socket(zmq.REQ)
        sock.setsockopt(zmq.LINGER, 10)
        sock.connect('tcp://' + iptools.ipv4.long2ip(ip_addr) + ':5555')
        if target and ip_addr and url:
            sock.send('url;' + target + ';' + str(url))
        sock.close()
        context.term()
    except Exception:
        pass

def send_chat_message(sendername, msg):
    """ Sends an entered chat message to all screen nodes.

        :param sendername: The name of the sender
        :type sendername: String
        :param msg: The message
        :type msg: String

        """
    nodes = Computer.objects.filter(time__gte=datetime.datetime.now() -
                                    timedelta(minutes=2), screens__gt=0)
    nodes = nodes.annotate(dcount=Count('name')).order_by('wos_id')
    for node in nodes:
        try:
            context = zmq.Context()
            sock = context.socket(zmq.REQ)
            sock.setsockopt(zmq.LINGER, 10)
            node_ip = iptools.ipv4.long2ip(int(node.ip))
            sys.stderr.write('SENDING MESSAGE TO: %s\n' % str(node_ip))
            sys.stderr.flush()
            sock.connect('tcp://' + node_ip + ':5555')
            if sendername and msg:
                sock.send('chatmsg;' + str(node.id) + ';' +
                            base64.b64encode((sendername + ':' + msg).encode(
                                                                    'utf-8')))
            sock.close()
            context.term()
        except Exception, err:
            sys.stderr.write('EXCEPTION: %s\n' % str(err))
            sys.stderr.flush()


def awake():
    """
    Sends WakeOnLAN packet to the MAC addresses in MACS.
    Also, turns on TV'sock (SHARP IP control).

    """
    # send wol packet to the machines
    for mac in MACS:
        iterator = iter(mac)
        mac_s = ':'.join(a + b for a, b in zip(iterator, iterator))
        wol.send_magic_packet(mac_s, broadcast='192.168.1.255')
    # turn on the tvs, switch to hdmi1
    for televisio in TVS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(televisio)
            sock.sendall(TV_COMMANDS['powr1'])
            sock.recv(9)
            sock.sendall(TV_COMMANDS['hdmi1'])
            sock.recv(9)
            sock.sendall(TV_COMMANDS['hdmi1'])
            sock.recv(9)
            sock.close()
        except Exception:
            pass


def snaphot(path, event_id):
    """
    Save a snapshot from the IP camera () to project's directory.

    :param path: Path to project's directory
    :type path: String

     """
    if path and event_id:
        path = os.path.join(PROJECTS_PATH, path[path.find('Projects') + 8:])
        path = os.path.join(path, 'Snapshots').replace('\\', '/')
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except:
            pass
        # HTTP request
        request = urllib2.Request("http://192.168.1.85/image/jpeg.cgi")
        # Encode username and password
        base64string = base64.encodestring('%s:%s' % (CAMERA_USERNAME,
                                                      CAMERA_PASSWORD))
        base64string = base64string.replace('\n', '')
        # Add encoded credentials to the request
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            data = urllib2.urlopen(request, timeout=10).read()
            strnow = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
            name = event_id + '_' + strnow + '.jpg'
            name = os.path.join(path, name)
            output = open(name, 'wb')
            output.write(data)
            output.close()
        except Exception:
            pass


def send_save_audio():
    """ Send save audio message to responsive node. """
    nodes = Computer.objects.filter(time__gte=datetime.datetime.now() -
                                    timedelta(minutes=2), responsive=1)
    nodes = nodes.annotate(dcount=Count('name')).order_by('wos_id')
    for node in nodes[0:1]:
        try:
            context = zmq.Context()
            sock = context.socket(zmq.REQ)
            sock.setsockopt(zmq.LINGER, 10)
            sock.connect('tcp://' + iptools.ipv4.long2ip(node.ip) + ':5555')
            sock.send('save_audio;0;0')
            sock.close()
            context.term()
        except Exception:
            pass


def send_screenshot():
    """ Send screenshot message to SCREEN nodes. """
    nodes = Computer.objects.filter(time__gte=datetime.datetime.now() -
                                    timedelta(minutes=2), screens__gt=0)
    nodes = nodes.annotate(dcount=Count('name')).order_by('wos_id')
    for node in nodes:
        try:
            context = zmq.Context()
            sock = context.socket(zmq.REQ)
            sock.setsockopt(zmq.LINGER, 10)
            sock.connect('tcp://' + iptools.ipv4.long2ip(node.ip) + ':5555')
            sock.send('screenshot;0;0')
            sock.close()
            context.term()
        except Exception:
            pass


def send_command(command):
    """
    Send command to SCREEN nodes.

    :param command: The command to send
    :type command: String

    """
    nodes = Computer.objects.filter(time__gte=datetime.datetime.now() -
                                    timedelta(minutes=2), screens__gt=0)
    nodes = nodes.annotate(dcount=Count('name')).order_by('wos_id')
    for node in nodes:
        try:
            context = zmq.Context()
            sock = context.socket(zmq.REQ)
            sock.setsockopt(zmq.LINGER, 10)
            sock.connect('tcp://' + iptools.ipv4.long2ip(node.ip) + ':5555')
            sock.send('command;0;%s' % command)
            sock.close()
            context.term()
        except Exception:
            pass


def ip_leases():
    """
    Return a list of IP address leases from ASUS RT-N56U router

    :rtype: list

    """
    # HTTP request
    request = urllib2.Request("http://192.168.1.1/device-map/clients.asp")
    # Encode username and pass
    base64string = base64.encodestring('%s:%s' % (ROUTER_USERNAME,
                                                  ROUTER_PASSWORD))
    base64string = base64string.replace('\n', '')
    # Add encoded username and pass to the request
    request.add_header("Authorization", "Basic %s" % base64string)
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
        key_value = dic[key]
        json += u'"' + key + '":'
        if isinstance(key_value, dict):
            key_value = [key_value]
        if key == "project":
            json += u"{"
        else:
            json += u"["
        for subkey_value in key_value:
            obj = key != "project"
            if obj:
                json += "{"
            for subsubkey_value in subkey_value:
                val = subkey_value[subsubkey_value]
                if hasattr(val, 'isoformat'):
                    val = val.isoformat()
                elif isinstance(val, unicode):
                    val = val.replace('"', '\"').replace('\\', '\\\\')
                elif isinstance(val, (int, long)):
                    val = str(val)
                else:
                    val = ''
                subkey_value[subsubkey_value] = val
                json += u'"' + subsubkey_value + u'":' + u'"' + val + u'",'
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
    json = json.replace('\n', '\\n').replace('\r', '\\r')
    return json


def get_event_files(event_id, directory):
    """
    Fetches files related to an event from project's directory.

    :param event_id: Database row id of an event.
    :type event_id: Integer

    :param directory: The project directory.
    :rtype: String

    """
    idx = directory.find('Projects')
    if idx == -1:
        return '[]'
    idx += 9
    dirn = os.path.join(PROJECTS_PATH, directory[idx:])
    dirn = dirn.replace('/', os.sep).replace('\\', os.sep)
    # idx = dirn.find('Projects') + 9
    if os.name == 'nt':
        dirn = r'\\' + dirn
    os.chdir(dirn)
    files = glob.glob("*%s%s_*" % (os.sep, event_id))
    out = []
    for filename in files:
        filepath = os.path.join('/static/Projects', directory[idx:], filename)
        filepath = filepath.encode('utf-8')
        if 'C:' in os.getcwd():
            filepath = filepath.replace('C:/', '/static/').replace('\\', '/')
        else:
            filepath = filepath.replace('share', 'static')
        out.append(filepath)
    return str(out).replace("'", '"')


def event_has_audio(event_id, directory):
    """
    Fetches audio files related to an event from project's directory.

    :param event_id: Database row id of an event.
    :type event_id: Integer

    :param directory: The project directory.
    :rtype: JSON String

    """
    idx = directory.find('Projects')
    if idx == -1:
        return '[]'
    idx += 9
    dirn = os.path.join(PROJECTS_PATH, directory[idx:])
    dirn = dirn.replace('/', os.sep).replace('\\', os.sep)
    if os.name == 'nt':
        dirn = r'\\' + dirn
    os.chdir(dirn)
    files = glob.glob("Audio%s%s_*" % (os.sep, event_id))
    json = {}
    for filename in files:
        item = os.path.join('/static/Projects', directory[idx:], filename)
        item = item.encode('utf-8').replace('\\', '/')
        elem = os.path.splitext(filename)[1][1:].encode('utf-8')
        json[elem] = item
    return '[' + str(json).replace("'", '"') + ']'
