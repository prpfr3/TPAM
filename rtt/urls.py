from django.urls import path, re_path
from . import views #The . indicates to import views from the current directory

app_name = 'rtt'
urlpatterns = [

    # Home page.
    #re_path(r'^$', views.index, name='index'),
    re_path(r'^$', views.getlocations, name='getlocations'),

    # Get departure times
    re_path(r'^gettimes/(?P<crscode>\w+)/$', views.gettimes, name='gettimes'),

    # Get livetimes
    re_path(r'^getlivefreight/(?P<crscode>\w+)/$', views.getlivefreight, name='getlivefreight'),

    re_path(r'^getlivepassenger/(?P<crscode>\w+)/$', views.getlivepassenger, name='getlivepassenger'),

    # Get service
    #re_path(r'^getservice/$', views.getservice, name='getservice'),
    re_path(r'^getservice/(?P<uid>\w+)/$', views.getservice, name='getservice'),

    # Get a list of locations for selection
    re_path(r'^getlocations/$', views.getlocations, name='getlocations'),

    # Get details of a single location
    re_path(r'^getlocation/(?P<location_id>\d+)$', views.getlocation, name='getlocation'),
]