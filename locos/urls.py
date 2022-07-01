from django.urls import include, path, re_path
from . import views

app_name = 'locos'

urlpatterns = [

    re_path(r'^$', views.index, name='index'),

    re_path(r'^cart_detail/$', views.cart_detail, name='cart_detail'),
    re_path(r'^cart_add/(?P<slide_id>\d+)/$', views.cart_add, name='cart_add'),
    re_path(r'^cart_remove/(?P<slide_id>\d+)/$', views.cart_remove, name='cart_remove'),

    re_path(r'^companies/$', views.companies, name='companies'),
    re_path(r'^company/(?P<company_id>\d+)/$', views.company, name='company'),

    re_path(r'^routes/$', views.routes, name='routes'),
    re_path(r'^routemap/(?P<route_id>\d+)/$', views.routemap, name='routemap'),

    re_path(r'^loco_classes/$', views.loco_classes, name='loco_classes'),
    re_path(r'^loco_classes/(?P<loco_class_id>\d+)/$', views.loco_class, name='loco_class'),

    re_path(r'^builders/$', views.builders, name='builders'),
    re_path(r'^builder/(?P<builder_id>\d+)/$', views.builder, name='builder'),

    re_path(r'^persons/$', views.persons, name='persons'),
    re_path(r'^persons_timeline/$', views.persons_timeline, name='persons_timeline'),
    re_path(r'^persons_vis_timeline/$', views.persons_vis_timeline, name='persons_vis_timeline'),

    re_path(r'^images/$', views.images, name='images'),
    re_path(r'^image/(?P<image_id>\d+)/$', views.image, name='image'),
    re_path(r'^new_image/$', views.new_image, name='new_image'),
    re_path(r'^edit_image/(?P<image_id>\d+)/$', views.edit_image, name='edit_image'),
 
    re_path(r'^slides/$', views.slides, name='slides'),
    re_path(r'^slide/(?P<slide_id>\d+)/$', views.slide, name='slide'),



    re_path(r'^storymaps/$', views.storymaps, name='storymaps'),
    re_path(r'^storymap/(?P<storymap_id>\d+)/$', views.storymap, name='storymap'),

    re_path(r'^storymap_references/$', views.storymap_references, name='storymap_references'),
    ]