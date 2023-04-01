from django.urls import path
from . import views

app_name = 'people'

urlpatterns = [

    path('', views.index, name='index'),

    path('people/', views.people, name='people'),
    path('people_timeline/', views.people_timeline, name='people_timeline'),
    path('people_vis_timeline/', views.people_vis_timeline, name='people_vis_timeline'),
    ]