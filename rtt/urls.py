from django.urls import path
from . import views

app_name = 'rtt'
urlpatterns = [
    path('', views.locations, name='locations'),
    path('times/<str:crscode>/', views.times, name='times'),
    path('livefreight/<str:crscode>/', views.livefreight, name='livefreight'),
    path('livepassenger/<str:crscode>/', views.livepassenger, name='livepassenger'),
    path('service/<str:uid>/', views.service, name='service'),
    path('locations/', views.locations, name='locations'),
    path('location/<str:crscode>/', views.location, name='location'),
]