from django.urls import path
from . import views

app_name = 'aircraft'

urlpatterns = [

    path('', views.index, name='index'), #Home Page

    path('create/', views.AirBMimage_create, name='create'),

    path('aircraft_classes/', views.aircraft_classes, name='aircraft_classes'),
    path('aircraft_class/<int:aircraft_class_id>/', views.aircraft_class, name='aircraft_class'),

    path('airimages/', views.airimages, name='airimages'),
    path('airimage/<int:airimage_id>/', views.airimage, name='airimage'),
    path('new_airimage/', views.new_airimage, name='new_airimage'),
    path('edit_airimage/<int:airimage_id>/', views.edit_airimage, name='edit_airimage'),
]