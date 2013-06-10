from django.db import models
from django.contrib.flatpages.models import FlatPage as FlatPageOld
from taggit.managers import TaggableManager


class Company(models.Model):
    """ Company model. """
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = u'company'
    
    def __unicode__(self):
        return self.name 

       
class User(models.Model):
    """ User model. """
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    
    class Meta:
        db_table = u'user'
        
    def __unicode__(self):
        return self.name    
 
        
class Project(models.Model):
    """ Project model. """
    name = models.CharField(max_length=50)
    company = models.ForeignKey(Company)
    dir = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=40, null=True, blank=True)
    
    class Meta:
        db_table = u'project'
    
    def __unicode__(self):
        return self.name

    
class Session(models.Model):
    """ Session model. """
    name = models.CharField(max_length=50, null=True, blank=True)
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
        if self.name:
            return self.name
        start = ''
        end = ''
        if self.starttime:
            start = self.starttime.strftime('%d.%m.%Y %H:%M')
        if self.endtime:
            end = self.endtime.strftime('%d.%m.%Y %H:%M')
        return '%s - %s' % (start, end)     


class Action(models.Model):
    name = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = u'action'
    
    def __unicode__(self):
        return self.name


class Computer(models.Model):
    name = models.CharField(max_length=50)
    ip = models.PositiveIntegerField(null=True, blank=True)
    mac = models.CharField(max_length=12, null=True, blank=True)
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
    desc = models.CharField(max_length=500,null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(Session, null=True, blank=True)
    title = models.CharField(max_length=40,null=False, blank=False)
    tags = TaggableManager(blank=True)
    
    class Meta:
        db_table = u'event'
    
    def __unicode__(self):
        return str(self.title)   


class File(models.Model):
    path = models.CharField(max_length=255)
    project = models.ForeignKey(Project, null=True, blank=True)
    tags = TaggableManager(blank=True)
    
    class Meta:
        db_table = u'file'
    
    def __unicode__(self):
        return self.path


class Fileaction(models.Model):
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
    project = models.ForeignKey(Project, null=True, db_column='Project',
                                blank=True)
    user = models.ForeignKey(User, null=True, db_column='User', blank=True) 
    
    class Meta:
        db_table = u'projectmembers'


class Activity(models.Model):
    project = models.ForeignKey(Project, related_name='activities')
    session = models.ForeignKey(Session, null=True, blank=True,
                                related_name='activities')
    active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        db_table = u'activity'

    def save(self, *args, **kwargs):
        super(Activity, self).save(*args, **kwargs) 

    @classmethod    
    def unset_all(act):
        qs = Activity.objects.filter(active=True)
        for item in qs:
            item.active=False
            item.save()    

    def __unicode__(self):
        return "%s - %s - %s" % (self.project.name, self.session,
                                 str(self.active))


class Sessioncomputers(models.Model):
    session = models.ForeignKey(Session, null=True, db_column='Session',
                                blank=True) 
    computer = models.ForeignKey(Computer, null=True, db_column='Computer',
                                 blank=True) 
    
    class Meta:
        db_table = u'sessioncomputers'


class Sessionparticipants(models.Model):
    session = models.ForeignKey(Session, null=True, db_column='Session',
                                blank=True) 
    user = models.ForeignKey(User, null=True, db_column='User', blank=True) 
    
    class Meta:
        db_table = u'sessionparticipants'


class ExtendedFlatPage(FlatPageOld):
    related = 'flatpage_predecessor'
    help1 = 'Page that this one should appear after (if any)'
    help2 = 'Text for link title attribute. Will show on link hover.'
    show_after = models.ForeignKey('ExtendedFlatPage', null=True, blank=True,
                                   default=None, related_name=related,
                                   help_text=help1)
    alt_text = models.CharField(max_length=30, null=True, blank=True,
                                help_text=help2)
