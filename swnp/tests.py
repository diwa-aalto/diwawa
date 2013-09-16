"""
Tests for SWNP module.

"""
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from swnp.models import Company,Project, Session, Activity, Event, Computer
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import json
import validictory
import datetime 
import time
import threading
import sys
import os
import shutil

from test_schemas import ProjectSchema, NodesJsonSchema, \
                    ActivityJsonSchema, ProjectJsonSchema, ProjectsJsonSchema                

# Disabling stderr and stdout
class NullDevice():
    def write(self, s):
        pass
sys.stderr = NullDevice()
sys.stdout = NullDevice()   
                
class ViewsTest(LiveServerTestCase):
    fixtures = ['testdata.json']
    
    @classmethod
    def create_project_files(cls, project_name):
        project_dir = os.path.join(os.getcwd(),project_name)
        os.makedirs(project_dir)
        project_file = project_dir + os.sep + project_name + '.txt'
        fh = open(project_file, 'a')
        fh.write('Testing file.')
        fh.close()
        return project_dir
    
    @classmethod
    def delete_project_files(cls, project_name):
        project_dir = os.path.join(os.getcwd(),project_name)
        shutil.rmtree(project_dir)
        
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        cls.project_name = 'Selenium'
        cls.project_dir = cls.create_project_files(cls.project_name)
        super(ViewsTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        cls.delete_project_files(cls.project_name)
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
       
    def test_projects_json_all(self):
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)
        try:
            json_response = json.loads(response.content)
            validictory.validate(json_response, ProjectsJsonSchema)
        except ValueError as err:
            self.fail('Not valid JSON.'+str(err))
        self.assertEqual(len(json_response), 
                         Project.objects.exclude(password__isnull=True).count())
        
        
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
        response = self.client.post(reverse('event'), 
                                    {'title':'test_title'}, 
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'ERROR')
    
    def test_event_creation_with_activity(self):
        p = Project.objects.get(pk=3)
        s = Session.objects.create(project=p, 
                                   starttime=datetime.datetime.now())
        Activity.objects.create(project=p, session=s, active=1 )
        response = self.client.post(reverse('event'), 
                                    {'title':'test_title'}, 
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
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
        response = self.client.get(reverse('activity'), 
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
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
        s = Session.objects.create(project=p, 
                                   starttime=datetime.datetime.now())
        a = Activity.objects.create(project=p, session=s, active=1 )
        response = self.client.get(reverse('activity'), 
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
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
        response = self.client.get(reverse('nodes'), 
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
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
        response = self.client.get(reverse('nodes'), 
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        try:
            json_response = json.loads(response.content)
            validictory.validate(json_response, NodesJsonSchema)
        except ValueError as err:
            self.fail('Not valid JSON.'+str(err))
        self.assertEqual(len(json_response), 3) 
        
    def test_web_index(self):
        """ Selenium test case with a walkthrough."""
        # Alice presses the button at DiWACS and the index page shows
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        WebDriverWait(self.selenium, 10).until(
        lambda driver: driver.find_element_by_tag_name('body')) 
        self.assertIn('Diwaamo', self.selenium.title)
        # She sees the DiWA logo at the upper right corner
        try:
            img = self.selenium.find_element_by_class_name('top_logo')
        except NoSuchElementException:
            self.fail('DiWa logo not found')
        # Alice starts the DiWaCS machines and three nodes show up next to 
        # the event button
        comps = Computer.objects.filter(id__lt=4)
        comps.update(time=datetime.datetime.now())
        [ c.save() for c in comps]
        selector = 'div#node_holder div img'
        WebDriverWait(self.selenium, 30).until(
        lambda driver: driver.find_elements_by_css_selector(selector))
        nodes = self.selenium.find_elements_by_css_selector(selector)
        self.assertEqual(len(nodes), 3)
        try:
            evt = self.selenium.find_element_by_id('new_default_event')
        except NoSuchElementException:
            self.fail('Event button not found.')
        # A project is selected
        try:
            p = Project.objects.create(name=self.project_name, 
                                       dir=self.project_dir, 
                                       company=Company.objects.get(pk=1))
            s = Session.objects.create(project=p)
            a = Activity.objects.create(project=p, session=s, active=1)
        except Exception as err:
            print err
        comps = Computer.objects.filter(id__lt=4)
        comps.update(time=datetime.datetime.now())
        [ c.save() for c in comps]
        WebDriverWait(self.selenium, 30).until(
        lambda driver: driver.find_element_by_id('selected_project').text 
                        == self.project_name)
        # and chat is enabled
        try:
            chat = self.selenium.find_element_by_id('fchat')
            self.assertEqual(chat.is_displayed(), True)
        except NoSuchElementException:
            self.fail('Chat form not found.')
        # Alice Drags a file from the folder and drops it to ORANGE node.
        ac = ActionChains(self.selenium)
        try:
            selector = 'div#filetree li:first-child a'
            source = self.selenium.find_element_by_css_selector(selector)
        except NoSuchElementException:
            time.sleep(15)
            self.fail('Source not found for DnD.')
            
        try:
            target = self.selenium.find_element_by_id('node2')
        except NoSuchElementException:
            self.fail('target not found for DnD.')
        ac.drag_and_drop(source, target) 
        # She clicks now the event button and chooses Important title
        try:
            selector = 'div#dropdown-1 ul li:first-child a'
            important  = self.selenium.find_element_by_css_selector(selector)
        except NoSuchElementException:
            self.fail('Important link not found.')
        evt.click()
        important.click()
        # After that she cliocks to Meeting Browser tab 
        mb = self.selenium.find_element_by_link_text('Meeting Browser')
        mb.click()
        WebDriverWait(self.selenium, 30).until(
        lambda driver: driver.find_element_by_id('mbprojects'))
        # and sees the timeline for the selected project 
        try:
            timeline = self.selenium.find_element_by_id('mytimeline')
            dropdown = Select(self.selenium.find_element_by_id("mbprojects"))
        except NoSuchElementException:
            self.fail('Timeline or dropdown not found.')
        self.assertEqual(dropdown.first_selected_option.text, 'Selenium')
        # She sees the event Important on the table. 
        imp_xpath = '//table[@id=\'all_events\']//td[contains(.,\'Important\')]'
        try:
            imp_td = self.selenium.find_element_by_xpath(imp_xpath)
        except NoSuchElementException:
            self.fail('Important event not found in the table.')
        self.assertEqual(imp_td.is_displayed(), True)

                