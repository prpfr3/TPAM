from django.urls import path
from . import views

app_name = 'rtt'
urlpatterns = [

    #path('', views.index, name='index'), #Out of Service until further menu entries needed
    path('', views.getlocations, name='getlocations'),
    path('gettimes/<str:crscode>/', views.gettimes, name='gettimes'),
    path('getlivefreight/<str:crscode>/', views.getlivefreight, name='getlivefreight'),
    path('getlivepassenger/<str:crscode>/', views.getlivepassenger, name='getlivepassenger'),
    path('getservice/<str:uid>/', views.getservice, name='getservice'),
    path('getlocations/', views.getlocations, name='getlocations'),
    # path('getlocation/<int:location_id>/', views.getlocation, name='getlocation'),
    path('getlocation/<str:crscode>/', views.getlocation, name='getlocation'),
]