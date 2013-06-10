from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('swnp.views',
    url(r'^$', 'index', name='home'),
    url(r'^mb/$', 'diwamb',name='diwamb'),
    url(r'^upload/(?P<computer_id>\d{1,3})/$', 'upload', name='upload'),
    url(r'^dirlist/$', 'dirlist', name='dirlist'),
    url(r'^chat/$', 'chat', name='chat'),
    url(r'^event/$', 'event', name='event'),
    url(r'^event_files/$', 'event_files', name='event_files'),
    url(r'^event_has_audio/$', 'has_audio', name='event_has_audio'),
    url(r'^nodes/$', 'nodes', name='nodes'),
    url(r'^projects/$', 'projects_json', name='projects'),
    url(r'^projects/(?P<project_id>\d+)/$', 'project_json', name='project'),
    url(r'^activity/$', 'activity', name='activity'),
    url(r'^awake/$', 'awake', name='awake'),
    url(r'^shutdown/$', 'shutdown', name='shutdown'),
    url(r'^openurl/(?P<computer_id>\d{1,3})/$', 'openurl', name='openurl'),
    url(r'^stats/$', 'stats', name='stats'),
    url(r'^event/(?P<event_id>\d+)/edit/$', 'edit_event', name='edit_event'),
    url(r'^chat/', include('jchat.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)

logout_url = url(r'^logout/$', 'django.contrib.auth.views.logout')
urlpatterns += patterns('', logout_url)

urlpatterns += staticfiles_urlpatterns()