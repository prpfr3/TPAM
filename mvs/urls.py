from django.urls import path
from . import views

app_name = 'mvs'

urlpatterns = [

    path('', views.index, name='index'), #Home Page

    path('create/', views.MVBMimage_create, name='create'),

    path('military_vehicle_classes/', views.military_vehicle_classes, name='military_vehicle_classes'),
    path('military_vehicle_class/<int:military_vehicle_class_id>/', views.military_vehicle_class, name='military_vehicle_class'),

    path('mvimages/', views.mvimages, name='mvimages'),
    path('mvimage/<int:mvimage_id>/', views.mvimage, name='mvimage'),
    path('new_mvimage/', views.new_mvimage, name='new_mvimage'),
    path('edit_mvimage/<int:mvimage_id>/', views.edit_mvimage, name='edit_mvimage'),

    path('thing/<int:pk>/favorite', views.AddFavoriteView.as_view(), name='mvclass_favorite'),
    path('thing/<int:pk>/unfavorite', views.DeleteFavoriteView.as_view(), name='mvclass_unfavorite'),

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