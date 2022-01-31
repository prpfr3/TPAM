from django.urls import re_path 
from django.conf import settings
from . import views

app_name = 'mainmenu'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
]

