from django.urls import path, re_path
from . import views

app_name = 'rtt'
urlpatterns = [

    #re_path(r'^$', views.index, name='index'), #Out of Service until further menu entries needed
    re_path(r'^$', views.getlocations, name='getlocations'),
    re_path(r'^gettimes/(?P<crscode>\w+)/$', views.gettimes, name='gettimes'),
    re_path(r'^getlivefreight/(?P<crscode>\w+)/$', views.getlivefreight, name='getlivefreight'),
    re_path(r'^getlivepassenger/(?P<crscode>\w+)/$', views.getlivepassenger, name='getlivepassenger'),
    re_path(r'^getservice/(?P<uid>\w+)/$', views.getservice, name='getservice'),
    re_path(r'^getlocations/$', views.getlocations, name='getlocations'),
    re_path(r'^getlocation/(?P<location_id>\d+)$', views.getlocation, name='getlocation'),
    re_path(r'^chooselocation$', views.chooselocation, name='chooselocation'),
]