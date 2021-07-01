from django.urls import path, re_path
from . import views

app_name = 'mvs'

urlpatterns = [

    re_path(r'^$', views.index, name='index'), #Home Page

    path('create/', views.MVBMimage_create, name='create'),

    re_path(r'^military_vehicle_classes/$', views.military_vehicle_classes, name='military_vehicle_classes'),
    re_path(r'^military_vehicle_class/(?P<military_vehicle_class_id>\d+)/$', views.military_vehicle_class, name='military_vehicle_class'),

    re_path(r'^mvimages/$', views.mvimages, name='mvimages'),
    re_path(r'^mvimage/(?P<mvimage_id>\d+)/$', views.mvimage, name='mvimage'),
    re_path(r'^new_mvimage/$', views.new_mvimage, name='new_mvimage'),
    re_path(r'^edit_mvimage/(?P<mvimage_id>\d+)/$', views.edit_mvimage, name='edit_mvimage'),

# Possible future design pattern
    #path('', views.xyz_list),
    #path('xyz/<slug:slug>/', include([
    #  path('', views.xyz_detail),
    #  path('add', views.xyz_add),
    #  path('delete', views.xyz_delete),
    #  path('edit', views.xyz_edit),
    #  ]))

    # or could use GET/POST/PUT/DELETE and build that into the view
]