from django.urls import path
from . import views

app_name = 'locos'

urlpatterns = [

    path('', views.index, name='index'),

    path('builders/', views.builders, name='builders'),
    path('builder/<int:builder_id>/', views.builder, name='builder'),

    path('companies/', views.companies, name='companies'),
    path('company/<int:company_id>/', views.company, name='company'),

    path('loco_classes/', views.loco_classes, name='loco_classes'),
    path('loco_classes/<int:loco_class_id>/', views.loco_class, name='loco_class'),

    path('locomotives/', views.locomotives, name='locomotives'),
    path('locomotive/<int:locomotive_id>/', views.locomotive, name='locomotive'),

    path('persons/', views.persons, name='persons'),
    path('persons_timeline/', views.persons_timeline, name='persons_timeline'),
    path('persons_vis_timeline/', views.persons_vis_timeline, name='persons_vis_timeline'),
    ]