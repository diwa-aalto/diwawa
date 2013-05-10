from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('swnp.views',
    # Examples:
    #(r'^tinymce/', include('tinymce.urls')),
    url(r'^$', 'index',{'template':'metro'}, name='home'),
    #url(r'^metro/$', 'index',{'template':'metro'},name='home'),
    url(r'^mb/$', 'diwamb',name='diwamb'),
    url(r'^upload/(?P<id>\d{1,3})/$', 'upload', name='upload'),
    url(r'^dirlist/$', 'dirlist', name='dirlist'),
    url(r'^chat/$', 'chat', name='chat'),
    url(r'^event/$', 'event', name='event'),
    url(r'^event_files/$', 'event_files', name='event_files'),
    url(r'^event_has_audio/$', 'has_audio', name='event_has_audio'),
    url(r'^snapshot/$', 'snapshot', name='snapshot'),
    url(r'^screenshot/$', 'screenshot', name='screenshot'),
    url(r'^nodes/$', 'nodes', name='nodes'),
    url(r'^projects/$', 'projects_json', name='projects'),
    url(r'^projects/(?P<id>\d+)/$', 'project_json', name='project'),
    url(r'^timeline/(?P<id>\d+)/$', 'project_timeline_json', name='project_timeline'),
    url(r'^project/select/$', 'project_select', name='project_select'),
    url(r'^activity/$', 'activity', name='activity'),
    url(r'^awake/$', 'awake', name='awake'),
    url(r'^shutdown/$', 'shutdown', name='shutdown'),
    url(r'^openurl/(?P<id>\d{1,3})/$', 'openurl', name='openurl'),
    url(r'^stats/$', 'stats', name='stats'),
    url(r'^event/(?P<event_id>\d+)/edit/$', 'edit_event', name='edit_event'),
    
    # url(r'^Chimaira/', include('Chimaira.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^chat/', include('jchat.urls')),
    (r'^ipcamera/start/$', 'ipcamera',{'command': 'start'}),
    (r'^ipcamera/stop/$', 'ipcamera',{'command': 'stop'}),
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',url(r'^logout/$', 'django.contrib.auth.views.logout'))

urlpatterns += staticfiles_urlpatterns()