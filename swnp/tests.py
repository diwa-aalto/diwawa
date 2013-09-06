"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.

"""
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from swnp.models import Company,Project, Session, Activity, Event, Computer
from selenium.webdriver.support.wait import WebDriverWait
import json
import validictory
import datetime 
ProjectSchema = {
        "type": ["object", "number"],
        "properties": {
            "id": {
                "description": "The unique identifier",
                "type": ["number","string"]
            },
            "name": {
                "type": "string"
            },
            "company": {
                "type": ["number","string"]
            },
            "password": {
                "type": [ "string", "null" ],
                "minLength": 0,
                "blank": True
            },
            "dir": {
                "type": "string"
            }
        }
    }
NodesJsonSchema = {
    "type":"array",
    "$schema": "http://json-schema.org/draft-03/schema",
    "items": {
            "type":"object",
            "properties":{
                "img": {
                    "type":"string"
                },
                "node": {
                    "type":"object",
                    "properties":{
                        "id": {
                            "type":"number"
                        },
                        "ip": {
                            "type":"number"
                        },
                        "mac": {
                            "type":"string"
                        },
                        "name": {
                            "type":"string"
                        },
                        "pgm_group": {
                            "type":"number"
                        },
                        "responsive": {
                            "type":"number"
                        },
                        "screens": {
                            "type":"number"
                        },
                        "time": {
                            "type":"string"
                        },
                        "user": {
                            "type":"null"
                        },
                        "wos_id": {
                            "type":"number"
                        }
                    }
                }
            
        }
    }
}

ActivityJsonSchema = {
    "type":"object",
    "$schema": "http://json-schema.org/draft-03/schema",
    "properties":{
        "project":ProjectSchema,
        "room": {
            "type":"number",
            "required":False
        },
        "session": {
            "type":["number","object"],
            "properties":{
                "endtime": {
                    "type":["string","null"],
                    "required":False
                },
                "id": {
                    "type":"number",
                    "required":False
                },
                "name": {
                    "type":["string","null"],
                    "required":False
                },
                "previous_session": {
                    "type":["number","null"],
                    "required":False
                },
                "project": {
                    "type":"number",
                    "required":False
                },
                "starttime": {
                    "type":"string"
                }
            }
        },
        "status": {
            "type":"string"
        }
    }
}

ProjectJsonSchema = {
    "type":"object",
    "$schema": "http://json-schema.org/draft-03/schema",
    "properties":{
        "events": {
            "type":"array",
            "items":
                {
                    "type":"object",
                    "properties":{
                        "desc": {
                            "type":"string"
                        },
                        "id": {
                            "type":"string"
                        },
                        "time": {
                            "type":"string"
                        },
                        "title": {
                            "type":"string"
                        }
                    }
                }
            

        },
        "fileactions": {
            "type":"array",
            "items":
                {
                    "type":"object",
                    "properties":{
                        "action__name": {
                            "type":"string"
                        },
                        "action_time": {
                            "type":"string"
                        },
                        "file__id": {
                            "type":"string"
                        },
                        "file__path": {
                            "type":"string"
                        },
                        "id": {
                            "type":"string"
                        }
                    }
                }
            

        },
        "project": ProjectSchema,
        "sessions": {
            "type":"array",
            "items":
                {
                    "type":"object",
                    "properties":{
                        "endtime": {
                            "type":"string"
                        },
                        "id": {
                            "type":"string"
                        },
                        "name": {
                            "type":"string"
                        },
                        "starttime": {
                            "type":"string"
                        }
                    }
                }
        }
    }
}

ProjectsJsonSchema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Projects set",
    "type": "array",
    "items": ProjectSchema
}


class ViewsTest(LiveServerTestCase):
    fixtures = ['testdata']
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(ViewsTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ViewsTest, cls).tearDownClass() 
       
    def test_projects_json_empty(self):
        Project.objects.all().delete()
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)
        try:
            json_response = json.loads(response.content)
            validictory.validate(json_response, ProjectsJsonSchema)
        except ValueError as err:
            self.fail('Not valid JSON.'+str(err))
        self.assertEqual(len(json_response), 0)
        print "empty done"
       
    def test_projects_json_all(self):
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)
        try:
            json_response = json.loads(response.content)
            validictory.validate(json_response, ProjectsJsonSchema)
        except ValueError as err:
            self.fail('Not valid JSON.'+str(err))
        self.assertEqual(len(json_response), Project.objects.exclude(password__isnull=True).count())
        
        
    def test_project_json(self):
        response = self.client.get(reverse('project', args=(3,)))
        self.assertEqual(response.status_code, 200)
        try:
            json_response = json.loads(response.content)
            validictory.validate(json_response, ProjectJsonSchema)
        except ValueError as err:
            self.fail('Not valid JSON.'+str(err))
    
    def test_project_json_with_non_existing(self):
        response = self.client.get(reverse('project', args=(0,)))
        self.assertEqual(response.status_code, 200)
        try:
            json_response = json.loads(response.content)
        except ValueError as err:
            self.fail('Not valid JSON.'+str(err))
        self.assertRaises(validictory.FieldValidationError, 
                          validictory.validate, json_response, 
                          ProjectJsonSchema)

    def test_event_creation_no_activity(self):
        response = self.client.post(reverse('event'), {'title':'test_title'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'ERROR')
    
    def test_event_creation_with_activity(self):
        p = Project.objects.get(pk=3)
        s = Session.objects.create(project=p, starttime=datetime.datetime.now())
        Activity.objects.create(project=p, session=s, active=1 )
        response = self.client.post(reverse('event'), {'title':'test_title'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'OK')
        event = Event.objects.latest('id')
        self.assertEqual(event.title, 'test_title')
        self.assertEqual(event.session, s)
        
    def test_activity_no_ajax(self):
        response = self.client.get(reverse('activity'))
        self.assertEqual(response.status_code, 200)
        try:
            json_response = json.loads(response.content)
        except ValueError as err:
            self.fail('Not valid JSON.'+str(err))
        self.assertEqual(json_response['status'], 'ERROR')   
    
    def test_activity_no_activity(self):
        response = self.client.get(reverse('activity'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        try:
            json_response = json.loads(response.content)
            validictory.validate(json_response, ActivityJsonSchema)
        except ValueError as err:
            self.fail('Not valid JSON.'+str(err))
        self.assertEqual(json_response['status'], 'OK')
        self.assertEqual(json_response['project'], 0)
        self.assertEqual(json_response['session'], 0)
    
    def test_activity_with_activity(self):
        p = Project.objects.get(pk=3)
        s = Session.objects.create(project=p, starttime=datetime.datetime.now())
        a = Activity.objects.create(project=p, session=s, active=1 )
        response = self.client.get(reverse('activity'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        try:
            json_response = json.loads(response.content)
            validictory.validate(json_response, ActivityJsonSchema)
        except ValueError as err:
            self.fail('Not valid JSON.'+str(err))     
        self.assertEqual(json_response['status'], 'OK')
        self.assertEqual(json_response['project']['id'], 3)
        self.assertEqual(json_response['session']['id'], s.id)
        
    def test_nodes_no_ajax(self):
        response = self.client.get(reverse('nodes'))
        self.assertEqual(response.status_code, 200)
        try:
            json_response = json.loads(response.content)
        except ValueError as err:
            self.fail('Not valid JSON.'+str(err))
        self.assertEqual(json_response['status'], 'ERROR')   
    
    def test_nodes_no_nodes(self):
        response = self.client.get(reverse('nodes'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        try:
            json_response = json.loads(response.content)
            validictory.validate(json_response, NodesJsonSchema)
        except ValueError as err:
            self.fail('Not valid JSON.'+str(err))
        self.assertEqual(len(json_response), 0)
        
    def test_nodes_with_nodes(self):
        nodes = Computer.objects.all().order_by('-id')[:3]
        for node in nodes:
            node.time = datetime.datetime.now()
            node.pgm_group = 1
            node.screens = 1
            node.save()
        response = self.client.get(reverse('nodes'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        try:
            json_response = json.loads(response.content)
            validictory.validate(json_response, NodesJsonSchema)
        except ValueError as err:
            self.fail('Not valid JSON.'+str(err))
        self.assertEqual(len(json_response), 3)  

    def test_web_index(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        WebDriverWait(self.selenium, 10).until(
        lambda driver: driver.find_element_by_tag_name('body')) 
        self.assertIn('Diwaamo', self.selenium.title)
        
            