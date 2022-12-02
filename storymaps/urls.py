from django.urls import include, path, re_path
from . import views

app_name = 'storymaps'

urlpatterns = [
    re_path(r'^storymaps/$', views.storymaps, name='storymaps'),
    re_path(r'^storymap/(?P<storymap_id>\d+)/$', views.storymap, name='storymap'),
    ]