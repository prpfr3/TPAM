from django.urls import include, path, re_path
from . import views

app_name = 'locos'

urlpatterns = [

    re_path(r'^$', views.index, name='index'),

    re_path(r'^loco_classes/$', views.loco_classes, name='loco_classes'),
    re_path(r'^loco_classes/(?P<loco_class_id>\d+)/$', views.loco_class, name='loco_class'),

    re_path(r'^modern_classes/$', views.modern_classes, name='modern_classes'),
    re_path(r'^modern_classes/(?P<modern_class_id>\d+)/$', views.modern_class, name='modern_class'),

    re_path(r'^engineers/$', views.engineers, name='engineers'),
    re_path(r'^engineers/(?P<engineer_id>\d+)/$', views.engineer, name='engineer'),
    re_path(r'^new_engineer/$', views.new_engineer, name='new_engineer'),
    re_path(r'^edit_engineer/(?P<engineer_id>\d+)/$', views.edit_engineer, name='edit_engineer'),

    re_path(r'^images/$', views.images, name='images'),
    re_path(r'^image/(?P<image_id>\d+)/$', views.image, name='image'),
    re_path(r'^new_image/$', views.new_image, name='new_image'),
    re_path(r'^edit_image/(?P<image_id>\d+)/$', views.edit_image, name='edit_image'),
    ]