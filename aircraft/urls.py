from django.urls import path, re_path
from . import views

app_name = 'aircraft'

urlpatterns = [

    re_path(r'^$', views.index, name='index'), #Home Page

    path('create/', views.AirBMimage_create, name='create'),

    re_path(r'^aircraft_classes/$', views.aircraft_classes, name='aircraft_classes'),
    re_path(r'^aircraft_class/(?P<aircraft_class_id>\d+)/$', views.aircraft_class, name='aircraft_class'),

    re_path(r'^airimages/$', views.airimages, name='airimages'),
    re_path(r'^airimage/(?P<airimage_id>\d+)/$', views.airimage, name='airimage'),
    re_path(r'^new_airimage/$', views.new_airimage, name='new_airimage'),
    re_path(r'^edit_airimage/(?P<airimage_id>\d+)/$', views.edit_airimage, name='edit_airimage'),
]