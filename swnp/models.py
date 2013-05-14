# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.contrib.flatpages.models import FlatPage as FlatPageOld
from taggit.managers import TaggableManager
class Company(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    class Meta:
        db_table = u'company'
    def __unicode__(self):
        return self.name    
class User(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=300, blank=True)
    title = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=300, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    class Meta:
        db_table = u'user'
        
    def __unicode__(self):
        return self.name    
        
class Project(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    company = models.ForeignKey(Company)
    dir = models.CharField(max_length=765, null=True, blank=True)
    password = models.CharField(max_length=120, null=True, blank=True)
    class Meta:
        db_table = u'project'
    def __unicode__(self):
        return self.name
    
class Session(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    project = models.ForeignKey(Project)
    starttime = models.DateTimeField(null=True, blank=True)
    endtime = models.DateTimeField(null=True, blank=True)
    previous_session = models.ForeignKey('self', null=True, blank=True)
    
    def get_duration(self):
        duration = self.starttime - self.endtime
        return duration.total_seconds()
    class Meta:
        db_table = u'session' 
    def __unicode__(self):
        return self.name if self.name else "%s - %s" % (self.starttime.strftime("%d.%m.%Y %H:%M") if self.starttime else "",self.endtime.strftime("%d.%m.%Y %H:%M") if self.endtime else "")     
class Action(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'action'
    def __unicode__(self):
        return self.name


class Computer(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    ip = models.PositiveIntegerField(null=True, blank=True)
    mac = models.CharField(max_length=36, null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    screens = models.IntegerField(null=True, blank=True)
    responsive = models.NullBooleanField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    wos_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'computer'
    def __unicode__(self):
        return self.name    

class Event(models.Model):
    #id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=1500,null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(Session, null=True, blank=True)
    title = models.CharField(max_length=120,null=True, blank=True)
    tags = TaggableManager(blank=True)
    class Meta:
        db_table = u'event'
    def __unicode__(self):
        return str(self.title)   

class File(models.Model):
    #id = models.IntegerField(primary_key=True)
    path = models.CharField(max_length=765)
    project = models.ForeignKey(Project, null=True, blank=True)
    tags = TaggableManager(blank=True)
    class Meta:
        db_table = u'file'
    def __unicode__(self):
        return self.path
class Fileaction(models.Model):
    #id = models.IntegerField(primary_key=True)
    file = models.ForeignKey(File)
    action = models.ForeignKey(Action)
    action_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    computer = models.ForeignKey(Computer, null=True, blank=True)
    session = models.ForeignKey(Session, null=True, blank=True)
    class Meta:
        db_table = u'fileaction'
    def __unicode__(self):
        return "%s:%s" % (self.action.name,self.file.path)
class Projectmembers(models.Model):
    project = models.ForeignKey(Project, null=True, db_column='Project', blank=True) # Field name made lowercase.
    user = models.ForeignKey(User, null=True, db_column='User', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'projectmembers'

class Activity(models.Model):
    project = models.ForeignKey(Project,related_name='activities')
    session = models.ForeignKey(Session, null=True, blank=True,related_name='activities')
    active = models.BooleanField(null=False,blank=False,default=True)
    class Meta:
        db_table = u'activity'
    def save(self, *args, **kwargs):
        super(Activity, self).save(*args, **kwargs) # Call the "real" save() method.
    @classmethod    
    def unset_all(act):
        qs = Activity.objects.filter(active=True)
        for item in qs:
            item.active=False
            item.save()    
    def __unicode__(self):
        return "%s - %s - %s" % (self.project.name,self.session,str(self.active))
class Sessioncomputers(models.Model):
    session = models.ForeignKey(Session, null=True, db_column='Session', blank=True) # Field name made lowercase.
    computer = models.ForeignKey(Computer, null=True, db_column='Computer', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'sessioncomputers'

class Sessionparticipants(models.Model):
    session = models.ForeignKey(Session, null=True, db_column='Session', blank=True) # Field name made lowercase.
    user = models.ForeignKey(User, null=True, db_column='User', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'sessionparticipants'

class ExtendedFlatPage(FlatPageOld):
    show_after = models.ForeignKey('ExtendedFlatPage', null=True, blank=True, default=None, related_name="flatpage_predecessor", help_text="Page that this one should appear after (if any)")
    alt_text = models.CharField(max_length=30, null=True, blank=True, help_text="Text for link title attribute. Will show on link hover.")
