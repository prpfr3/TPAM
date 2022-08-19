from django.urls import re_path
from django.conf import settings
from django.views.generic import TemplateView
from . import views

app_name = 'D3'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
]